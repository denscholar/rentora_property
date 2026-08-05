from collections.abc import Iterable
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from properties.models import Amenity, PropertySubmission


# =====================================================
# SERVICE CONSTANTS
# =====================================================
EDITABLE_SUBMISSION_STATUSES = {
    PropertySubmission.Status.DRAFT,
    PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
}

SUBMITTABLE_SUBMISSION_STATUSES = {
    PropertySubmission.Status.DRAFT,
    PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
}

ARCHIVABLE_SUBMISSION_STATUSES = {
    PropertySubmission.Status.DRAFT,
    PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
}

ALLOWED_SUBMISSION_SOURCES = {
    PropertySubmission.Source.AGENT,
    PropertySubmission.Source.LANDLORD,
    PropertySubmission.Source.ADMIN,
}

SUBMISSION_UPDATE_FIELDS = {
    "property_type",
    "purpose",
    "property_condition",
    "furnishing_status",
    "area",
    "payment_frequency",
    "title",
    "description",
    "landmark",
    "street_address",
    "bedrooms",
    "bathrooms",
    "toilets",
    "parking_spaces",
    "floors",
    "units_available",
    "year_built",
    "is_new_build",
    "is_serviced",
    "is_negotiable",
    "land_size",
    "building_size",
    "size_unit",
    "available_from",
    "minimum_stay",
    "proposed_price",
    "service_charge",
    "caution_fee",
    "legal_fee",
    "agency_fee",
    "latitude",
    "longitude",
}


# =====================================================
# INTERNAL HELPERS
# =====================================================
def _get_user_role_value(user) -> str:
    """
    Returns a normalized role value from the authenticated user.

    Supports role implementations where user.role may be:
    - a string;
    - a model containing a slug;
    - a model containing a name;
    - a user model exposing account_type instead of role.
    """

    role = getattr(user, "role", None)

    if role is None:
        role = getattr(user, "account_type", None)

    if role is None:
        raise ValidationError(
            {
                "role": (
                    "Your account does not have a role and cannot "
                    "submit properties."
                )
            }
        )

    if isinstance(role, str):
        role_value = role
    else:
        role_value = (
            getattr(role, "slug", None)
            or getattr(role, "code", None)
            or getattr(role, "name", None)
        )

    if not role_value:
        raise ValidationError(
            {"role": "Unable to determine your account role."}
        )

    return str(role_value).strip().lower().replace(" ", "_")


def _get_submission_source(user) -> str:
    """
    Determines the submission source from the user's actual account role.

    The source is never accepted from frontend input because users must not
    be allowed to impersonate agents, landlords, or administrators.
    """

    role_value = _get_user_role_value(user)

    role_source_mapping = {
        "agent": PropertySubmission.Source.AGENT,
        "landlord": PropertySubmission.Source.LANDLORD,
        "admin": PropertySubmission.Source.ADMIN,
        "administrator": PropertySubmission.Source.ADMIN,
        "super_admin": PropertySubmission.Source.ADMIN,
        "superadmin": PropertySubmission.Source.ADMIN,
    }

    source = role_source_mapping.get(role_value)

    if source not in ALLOWED_SUBMISSION_SOURCES:
        raise ValidationError(
            {
                "role": (
                    "Only agents, landlords, and administrators may "
                    "submit properties."
                )
            }
        )

    return source


def _validate_submission_owner(
    *,
    submission: PropertySubmission,
    user,
) -> None:
    """
    Ensures the submission belongs to the requesting user.

    Administrators are not automatically allowed to edit another user's
    submission through this owner-facing service. Admin moderation should
    use separate review service functions.
    """

    if submission.submitted_by_id != user.pk:
        raise ValidationError(
            {
                "submission": (
                    "You do not have permission to modify this "
                    "property submission."
                )
            }
        )


def _validate_submission_is_editable(
    submission: PropertySubmission,
) -> None:
    """
    Prevents modification after a submission enters the review workflow.
    """

    if submission.status not in EDITABLE_SUBMISSION_STATUSES:
        raise ValidationError(
            {
                "status": (
                    f"A submission with status "
                    f"'{submission.get_status_display()}' cannot be edited."
                )
            }
        )


def _validate_submission_is_submittable(
    submission: PropertySubmission,
) -> None:
    """
    Ensures the submission is in a status that may transition to SUBMITTED.
    """

    if submission.status not in SUBMITTABLE_SUBMISSION_STATUSES:
        raise ValidationError(
            {
                "status": (
                    f"A submission with status "
                    f"'{submission.get_status_display()}' cannot be submitted."
                )
            }
        )


def _validate_submission_is_archivable(
    submission: PropertySubmission,
) -> None:
    """
    Restricts user-driven archiving to drafts and submissions returned for
    more information.
    """

    if submission.status not in ARCHIVABLE_SUBMISSION_STATUSES:
        raise ValidationError(
            {
                "status": (
                    f"A submission with status "
                    f"'{submission.get_status_display()}' cannot be archived."
                )
            }
        )


def _validate_amenities(
    amenities: Iterable[Amenity] | None,
) -> list[Amenity]:
    """
    Validates and normalizes amenities before assigning the M2M relation.

    The serializer should normally supply Amenity model instances.
    """

    if amenities is None:
        return []

    normalized_amenities = list(amenities)

    invalid_amenities = [
        amenity
        for amenity in normalized_amenities
        if not isinstance(amenity, Amenity)
    ]

    if invalid_amenities:
        raise ValidationError(
            {
                "amenities": (
                    "Every amenity must be a valid Amenity instance."
                )
            }
        )

    inactive_amenities = [
        amenity.name
        for amenity in normalized_amenities
        if not amenity.is_active
    ]

    if inactive_amenities:
        raise ValidationError(
            {
                "amenities": (
                    "Inactive amenities cannot be selected: "
                    f"{', '.join(inactive_amenities)}."
                )
            }
        )

    return normalized_amenities


def _set_submission_fields(
    *,
    submission: PropertySubmission,
    data: dict[str, Any],
) -> list[str]:
    """
    Applies only explicitly permitted fields to a submission.

    Protected workflow fields such as status, source, submitted_by,
    reviewed_by, and approved_property cannot be changed through user input.

    Returns the names of fields that were changed.
    """

    changed_fields = []

    for field_name, value in data.items():
        if field_name not in SUBMISSION_UPDATE_FIELDS:
            continue

        if getattr(submission, field_name) != value:
            setattr(submission, field_name, value)
            changed_fields.append(field_name)

    return changed_fields


def _validate_submission_for_review(
    submission: PropertySubmission,
) -> None:
    """
    Performs strict business validation before review submission.

    Drafts may remain incomplete, but a submission entering the review queue
    must contain all essential property information.
    """

    errors = {}

    required_fields = {
        "property_type": "Property type is required.",
        "purpose": "Property purpose is required.",
        "property_condition": "Property condition is required.",
        "furnishing_status": "Furnishing status is required.",
        "area": "Property area is required.",
        "title": "Property title is required.",
        "description": "Property description is required.",
        "street_address": "Street address is required.",
        "proposed_price": "Proposed price is required.",
    }

    for field_name, error_message in required_fields.items():
        value = getattr(submission, field_name, None)

        if value is None or (
            isinstance(value, str) and not value.strip()
        ):
            errors[field_name] = error_message

    if (
        submission.proposed_price is not None
        and submission.proposed_price <= 0
    ):
        errors["proposed_price"] = (
            "Proposed price must be greater than zero."
        )

    if submission.units_available < 1:
        errors["units_available"] = (
            "At least one property unit must be available."
        )

    if submission.minimum_stay is not None:
        if submission.minimum_stay < 1:
            errors["minimum_stay"] = (
                "Minimum stay must be at least one."
            )

    current_year = timezone.now().year

    if submission.year_built is not None:
        if submission.year_built > current_year:
            errors["year_built"] = (
                "Year built cannot be later than the current year."
            )

    if errors:
        raise ValidationError(errors)


# =====================================================
# CREATE SUBMISSION DRAFT
# =====================================================
@transaction.atomic
def create_submission_draft(
    *,
    user,
    data: dict[str, Any] | None = None,
    amenities: Iterable[Amenity] | None = None,
) -> PropertySubmission:
    """
    Creates an incomplete property submission owned by the authenticated user.

    Draft creation is intentionally permissive because the user may complete
    the submission through multiple frontend wizard steps.
    """

    if not user or not user.is_authenticated:
        raise ValidationError(
            {"user": "Authentication is required."}
        )

    source = _get_submission_source(user)
    data = dict(data or {})

    # These values are controlled by the service, not the frontend.
    data.pop("submitted_by", None)
    data.pop("source", None)
    data.pop("status", None)
    data.pop("reviewed_by", None)
    data.pop("reviewed_at", None)
    data.pop("review_note", None)
    data.pop("approved_property", None)
    data.pop("possible_duplicate_property", None)
    data.pop("duplicate_similarity_score", None)
    data.pop("amenities", None)

    submission = PropertySubmission(
        submitted_by=user,
        source=source,
        status=PropertySubmission.Status.DRAFT,
    )

    _set_submission_fields(
        submission=submission,
        data=data,
    )

    # Model-level validation catches invalid choices, negative counters,
    # and other field errors while excluding M2M relations.
    submission.full_clean()
    submission.save()

    if amenities is not None:
        valid_amenities = _validate_amenities(amenities)
        submission.amenities.set(valid_amenities)

    return submission


# =====================================================
# UPDATE SUBMISSION DRAFT
# =====================================================
@transaction.atomic
def update_submission_draft(
    *,
    submission: PropertySubmission,
    user,
    data: dict[str, Any] | None = None,
    amenities: Iterable[Amenity] | None = None,
) -> PropertySubmission:
    """
    Updates an existing draft or a submission returned for more information.

    Workflow-controlled fields are ignored and cannot be altered through this
    function.
    """

    _validate_submission_owner(
        submission=submission,
        user=user,
    )
    _validate_submission_is_editable(submission)

    # Lock the current database row to prevent concurrent updates.
    submission = (
        PropertySubmission.objects.select_for_update()
        .get(pk=submission.pk)
    )

    _validate_submission_owner(
        submission=submission,
        user=user,
    )
    _validate_submission_is_editable(submission)

    data = dict(data or {})

    protected_fields = {
        "submitted_by",
        "source",
        "status",
        "reviewed_by",
        "reviewed_at",
        "review_note",
        "approved_property",
        "possible_duplicate_property",
        "duplicate_similarity_score",
        "amenities",
    }

    for protected_field in protected_fields:
        data.pop(protected_field, None)

    changed_fields = _set_submission_fields(
        submission=submission,
        data=data,
    )

    submission.full_clean()

    if changed_fields:
        submission.save(
            update_fields=[
                *changed_fields,
                "updated_at",
            ]
        )

    # None means the client did not send amenities.
    # An empty list means the client intentionally removed all amenities.
    if amenities is not None:
        valid_amenities = _validate_amenities(amenities)
        submission.amenities.set(valid_amenities)

    return submission


# =====================================================
# SUBMIT PROPERTY SUBMISSION
# =====================================================
@transaction.atomic
def submit_property_submission(
    *,
    submission: PropertySubmission,
    user,
) -> PropertySubmission:
    """
    Validates a completed draft and places it in the admin review queue.

    Valid transitions:

        DRAFT -> SUBMITTED

        MORE_INFORMATION_REQUIRED -> SUBMITTED
    """

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    submission = (
        PropertySubmission.objects.select_for_update()
        .select_related(
            "submitted_by",
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
            "area",
        )
        .prefetch_related("amenities")
        .get(pk=submission.pk)
    )

    _validate_submission_owner(
        submission=submission,
        user=user,
    )
    _validate_submission_is_submittable(submission)
    _validate_submission_for_review(submission)

    submission.status = PropertySubmission.Status.SUBMITTED

    # Clear the previous moderation response when corrected information
    # is resubmitted.
    submission.review_note = ""
    submission.reviewed_by = None
    submission.reviewed_at = None

    submission.full_clean()

    submission.save(
        update_fields=[
            "status",
            "review_note",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]
    )

    return submission


# =====================================================
# ARCHIVE SUBMISSION DRAFT
# =====================================================
@transaction.atomic
def archive_submission_draft(
    *,
    submission: PropertySubmission,
    user,
) -> PropertySubmission:
    """
    Soft-archives a draft instead of permanently deleting it.

    Submitted, approved, rejected, or under-review records are preserved for
    moderation and audit purposes.
    """

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    submission = (
        PropertySubmission.objects.select_for_update()
        .get(pk=submission.pk)
    )

    _validate_submission_owner(
        submission=submission,
        user=user,
    )
    _validate_submission_is_archivable(submission)

    if getattr(submission, "is_archived", False):
        raise ValidationError(
            {"submission": "This property submission is already archived."}
        )

    # Uses the archive behaviour supplied by SoftArchiveMixin.
    submission.archive()

    return submission