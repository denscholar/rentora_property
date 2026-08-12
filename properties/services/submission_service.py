from collections.abc import Iterable
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from properties.models.lookups.amenity import Amenity
from properties.models.property.media import PropertySubmissionMedia
from properties.models.property.submission import PropertySubmission

# =====================================================

# SERVICE CONSTANTS

# =====================================================

# -----------------------------------------------------

# EDITABLE STATUSES

# -----------------------------------------------------

# A user can only continue editing:

#

# 1. A draft

# 2. A submission that the admin/moderator returned

# because more information is required.

#

# Once a submission enters UNDER_REVIEW, it is locked

# from user-side editing.

#

# APPROVED and REJECTED submissions are also not editable

# through the normal owner-facing submission service.

# -----------------------------------------------------

EDITABLE_SUBMISSION_STATUSES = {
    PropertySubmission.Status.DRAFT,
    PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
}

# -----------------------------------------------------

# SUBMITTABLE STATUSES

# -----------------------------------------------------

# These are the only statuses from which a user can

# submit a property for review.

#

# IMPORTANT:

# There is NO SUBMITTED status anymore.

#

# The moment the user submits a completed draft, it

# immediately becomes UNDER_REVIEW.

# -----------------------------------------------------

SUBMITTABLE_SUBMISSION_STATUSES = {
    PropertySubmission.Status.DRAFT,
    PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
}

# -----------------------------------------------------

# ARCHIVABLE STATUSES

# -----------------------------------------------------

# Only APPROVED properties can be archived.

#

# A DRAFT cannot be archived through this service.

# A MORE_INFORMATION_REQUIRED submission cannot be archived.

# An UNDER_REVIEW submission cannot be archived.

# A REJECTED submission cannot be archived.

#

# This matches the business rule:

#

# Only an approved property can be archived.

# -----------------------------------------------------

ARCHIVABLE_SUBMISSION_STATUSES = {
    PropertySubmission.Status.APPROVED,
}

# -----------------------------------------------------

# ALLOWED SUBMISSION SOURCES

# -----------------------------------------------------

ALLOWED_SUBMISSION_SOURCES = {
    PropertySubmission.Source.AGENT,
    PropertySubmission.Source.LANDLORD,
    PropertySubmission.Source.ADMIN,
}

# -----------------------------------------------------

# USER-EDITABLE SUBMISSION FIELDS

# -----------------------------------------------------

# Workflow fields such as status, source, reviewer,

# review note, etc. are intentionally NOT included here.

#

# The frontend must never be able to directly manipulate

# the submission workflow.

# -----------------------------------------------------

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
    - a model containing a code;
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
                    "Your account does not have a role and cannot " "submit properties."
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
        raise ValidationError({"role": "Unable to determine your account role."})

    return str(role_value).strip().lower().replace(" ", "_")


def _get_submission_source(user) -> str:
    """
    Determines the submission source from the authenticated
    user's actual account role.

    ```
    The source is NEVER accepted from frontend input.

    This prevents a user from pretending to submit as another
    type of account.
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
                    "Only agents, landlords, and administrators "
                    "may submit properties."
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

    ```
    Administrators are NOT automatically allowed to modify
    another user's submission through this owner-facing service.

    Admin moderation should use separate moderation/review
    service functions.
    """

    if submission.submitted_by_id != user.pk:
        raise ValidationError(
            {
                "submission": (
                    "You do not have permission to modify " "this property submission."
                )
            }
        )


def _validate_submission_is_editable(
    submission: PropertySubmission,
) -> None:
    """
    Prevents modification after a submission enters the
    review workflow.

    ```
    Editable:

        DRAFT
        MORE_INFORMATION_REQUIRED

    Not editable:

        UNDER_REVIEW
        APPROVED
        REJECTED
    """

    if submission.status not in EDITABLE_SUBMISSION_STATUSES:
        raise ValidationError(
            {
                "status": (
                    f"A submission with status "
                    f"'{submission.get_status_display()}' "
                    "cannot be edited."
                )
            }
        )


def _validate_submission_is_submittable(
    submission: PropertySubmission,
) -> None:
    """
    Ensures the submission is in a status that can be
    sent into the review workflow.

    ```
    IMPORTANT:

    There is no SUBMITTED state.

    The transition is:

        DRAFT
            ↓
        UNDER_REVIEW

    or:

        MORE_INFORMATION_REQUIRED
            ↓
        UNDER_REVIEW
    """

    if submission.status not in SUBMITTABLE_SUBMISSION_STATUSES:
        raise ValidationError(
            {
                "status": (
                    f"A submission with status "
                    f"'{submission.get_status_display()}' "
                    "cannot be submitted for review."
                )
            }
        )


def _validate_submission_is_archivable(
    submission: PropertySubmission,
) -> None:
    """
    Ensures that only an APPROVED property can be archived.

    ```
    Workflow:

        APPROVED
            ↓
        ARCHIVED

    All other submission states remain protected.
    """

    if submission.status not in ARCHIVABLE_SUBMISSION_STATUSES:
        raise ValidationError(
            {
                "status": (
                    f"A submission with status "
                    f"'{submission.get_status_display()}' "
                    "cannot be archived. "
                    "Only approved properties can be archived."
                )
            }
        )


def _validate_amenities(
    amenities: Iterable[Amenity] | None,
) -> list[Amenity]:
    """
    Validates and normalizes amenities before assigning
    the ManyToMany relationship.

    ```
    The serializer should normally provide Amenity instances.
    """

    if amenities is None:
        return []

    normalized_amenities = list(amenities)

    invalid_amenities = [
        amenity for amenity in normalized_amenities if not isinstance(amenity, Amenity)
    ]

    if invalid_amenities:
        raise ValidationError(
            {"amenities": ("Every amenity must be a valid Amenity instance.")}
        )

    inactive_amenities = [
        amenity.name for amenity in normalized_amenities if not amenity.is_active
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

    ```
    Workflow-controlled fields such as:

        status
        source
        submitted_by
        reviewed_by
        reviewed_at
        review_note

    cannot be modified through user input.

    Returns the names of fields that changed.
    """

    changed_fields = []

    for field_name, value in data.items():

        # Ignore anything that isn't part of the user-editable
        # property data.
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
    Performs strict business validation before a submission
    enters UNDER_REVIEW.

    ```
    A draft can remain incomplete.

    However, once the user clicks "Submit", all essential
    property information must be available.
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

        value = getattr(
            submission,
            field_name,
            None,
        )

        if value is None or (isinstance(value, str) and not value.strip()):
            errors[field_name] = error_message

    if submission.proposed_price is not None and submission.proposed_price <= 0:
        errors["proposed_price"] = "Proposed price must be greater than zero."

    if submission.units_available < 1:
        errors["units_available"] = "At least one property unit must be available."

    if submission.minimum_stay is not None:

        if submission.minimum_stay < 1:
            errors["minimum_stay"] = "Minimum stay must be at least one."

    current_year = timezone.now().year

    if submission.year_built is not None:

        if submission.year_built > current_year:
            errors["year_built"] = (
                "Year built cannot be later than " "the current year."
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
    Creates an incomplete property submission owned by
    the authenticated user.

    ```
    New submissions ALWAYS start as DRAFT.

    The frontend cannot choose the initial status.
    """

    if not user or not user.is_authenticated:
        raise ValidationError({"user": "Authentication is required."})

    source = _get_submission_source(user)

    data = dict(data or {})

    # -------------------------------------------------
    # Remove all workflow-controlled fields.
    # -------------------------------------------------
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
        # -------------------------------------------------
        # Every new property submission starts as DRAFT.
        # It will only become UNDER_REVIEW when the user
        # explicitly submits it.
        # -------------------------------------------------
        status=PropertySubmission.Status.DRAFT,
    )

    _set_submission_fields(
        submission=submission,
        data=data,
    )

    # Model-level validation catches invalid choices,
    # negative values and other model constraints.
    submission.full_clean()
    submission.save()

    if amenities is not None:

        valid_amenities = _validate_amenities(
            amenities,
        )

        submission.amenities.set(
            valid_amenities,
        )

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
    Updates an existing DRAFT or
    MORE_INFORMATION_REQUIRED submission.

    ```
    UNDER_REVIEW, APPROVED and REJECTED submissions
    cannot be modified through this service.
    """

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    _validate_submission_is_editable(
        submission,
    )

    # Lock the current database row to prevent concurrent
    # updates.
    submission = PropertySubmission.objects.select_for_update().get(pk=submission.pk)

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    _validate_submission_is_editable(
        submission,
    )

    data = dict(data or {})

    # -------------------------------------------------
    # These fields belong to the workflow and must never
    # be controlled by the frontend.
    # -------------------------------------------------
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
        data.pop(
            protected_field,
            None,
        )

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
    #
    # An empty list means the client intentionally
    # removed all amenities.
    if amenities is not None:

        valid_amenities = _validate_amenities(
            amenities,
        )

        submission.amenities.set(
            valid_amenities,
        )

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
    Validates a completed draft and moves it directly
    into the UNDER_REVIEW workflow.

    ```
    IMPORTANT:

    There is intentionally NO SUBMITTED status.

    The lifecycle is:

        DRAFT
        ↓
        UNDER_REVIEW

    or:

        MORE_INFORMATION_REQUIRED
        ↓
        UNDER_REVIEW
    """

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    submission = PropertySubmission.objects.select_for_update().get(pk=submission.pk)

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    # -------------------------------------------------
    # Make sure the current status is allowed to enter
    # the review workflow.
    #
    # DRAFT -> UNDER_REVIEW
    # MORE_INFORMATION_REQUIRED -> UNDER_REVIEW
    # -------------------------------------------------
    _validate_submission_is_submittable(
        submission,
    )

    # -------------------------------------------------
    # Perform the strict validation required before
    # entering UNDER_REVIEW.
    # -------------------------------------------------
    _validate_submission_for_review(
        submission,
    )

    # -------------------------------------------------
    # IMPORTANT:
    #
    # We DO NOT set:
    #
    #     PropertySubmission.Status.SUBMITTED
    #
    # because that status no longer exists in the
    # business workflow.
    #
    # Submission immediately enters UNDER_REVIEW.
    # -------------------------------------------------
    submission.status = PropertySubmission.Status.UNDER_REVIEW

    # -------------------------------------------------
    # Clear any previous moderation response.
    #
    # This is important when an admin previously returned
    # the property with MORE_INFORMATION_REQUIRED and
    # the owner has now corrected the property.
    # -------------------------------------------------
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

# ARCHIVE APPROVED PROPERTY SUBMISSION

# =====================================================


@transaction.atomic
def archive_submission_draft(
    *,
    submission: PropertySubmission,
    user,
) -> PropertySubmission:
    """
    Archives an approved property submission.

    ```
    IMPORTANT:

    Despite the historical function name
    `archive_submission_draft`, this function now handles
    APPROVED submissions only.

    Only:

        APPROVED -> ARCHIVED

    is allowed.

    DRAFT, UNDER_REVIEW, REJECTED and
    MORE_INFORMATION_REQUIRED submissions cannot be
    archived.
    """

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    # Lock the row so two archive requests cannot race.
    submission = PropertySubmission.objects.select_for_update().get(pk=submission.pk)

    _validate_submission_owner(
        submission=submission,
        user=user,
    )

    # -------------------------------------------------
    # Only APPROVED submissions can be archived.
    #
    # This is the backend enforcement of the business
    # rule. Even if somebody manually calls the endpoint,
    # the backend will reject every non-approved status.
    # -------------------------------------------------
    _validate_submission_is_archivable(
        submission,
    )

    # -------------------------------------------------
    # Prevent duplicate archive operations.
    # -------------------------------------------------
    if getattr(
        submission,
        "is_archived",
        False,
    ):
        raise ValidationError(
            {"submission": ("This property submission is already archived.")}
        )

    # -------------------------------------------------
    # SoftArchiveMixin handles the actual archive
    # operation.
    #
    # This should NOT physically delete the record.
    # -------------------------------------------------
    submission.archive()

    return submission


# =====================================================

# SUBMISSION VALIDATION ERROR

# =====================================================


class PropertySubmissionSubmitError(Exception):
    """
    Raised when a property submission cannot be submitted.
    """

    pass


# =====================================================

# SUBMISSION MISSING-FIELDS HELPER

# =====================================================


def _get_submission_missing_fields(
    submission: PropertySubmission,
) -> dict[str, str]:
    """
    Returns the fields that must be completed before
    the submission can enter UNDER_REVIEW.
    """

    missing_fields = {}

    required_fields = {
        "property_type": "Property type is required.",
        "purpose": "Property purpose is required.",
        "title": "Property title is required.",
        "area": "Property area is required.",
        "street_address": "Street address is required.",
        "property_condition": "Property condition is required.",
        "furnishing_status": "Furnishing status is required.",
        "proposed_price": "Proposed price is required.",
        "payment_frequency": "Payment frequency is required.",
    }

    for field_name, message in required_fields.items():

        value = getattr(
            submission,
            field_name,
            None,
        )

        if value in {
            None,
            "",
        }:
            missing_fields[field_name] = message

    # -------------------------------------------------
    # A property must have at least one successfully
    # uploaded image before entering UNDER_REVIEW.
    # -------------------------------------------------
    completed_images_exist = submission.media.filter(
        media_type=(PropertySubmissionMedia.MediaType.IMAGE),
        upload_status=(PropertySubmissionMedia.UploadStatus.COMPLETED),
    ).exists()

    if not completed_images_exist:

        missing_fields["images"] = "Upload at least one property image."

    # -------------------------------------------------
    # At least one completed image must be selected as
    # the property's cover image.
    # -------------------------------------------------
    cover_image_exists = submission.media.filter(
        media_type=(PropertySubmissionMedia.MediaType.IMAGE),
        upload_status=(PropertySubmissionMedia.UploadStatus.COMPLETED),
        is_cover=True,
    ).exists()

    if completed_images_exist and not cover_image_exists:
        missing_fields["cover_image"] = "Select a cover image."

    return missing_fields


# =====================================================

# SUBMIT PROPERTY SUBMISSION

# =====================================================


@transaction.atomic
def submit_property_submission_with_media_validation(
    *,
    submission: PropertySubmission,
    user,
) -> PropertySubmission:
    """
    Alternative submission function that also performs
    the media-specific validation.

    ```
    This function exists so that the submission endpoint
    can enforce image and cover-image requirements.

    IMPORTANT:

        DRAFT
        ↓
        UNDER_REVIEW

    There is NO SUBMITTED state.
    """

    submission = PropertySubmission.objects.select_for_update().get(pk=submission.pk)

    # -------------------------------------------------
    # Ownership check.
    # -------------------------------------------------
    if submission.submitted_by_id != user.id:

        raise PropertySubmissionSubmitError("You do not own this property submission.")

    # -------------------------------------------------
    # Only DRAFT and MORE_INFORMATION_REQUIRED can
    # enter the review workflow.
    # -------------------------------------------------
    if submission.status not in {
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
    }:

        raise PropertySubmissionSubmitError(
            "This property submission cannot be submitted " "in its current status."
        )

    # -------------------------------------------------
    # Validate all required fields and uploaded media.
    # -------------------------------------------------
    missing_fields = _get_submission_missing_fields(
        submission,
    )

    if missing_fields:

        error = PropertySubmissionSubmitError(
            "Complete all required property information " "before submitting."
        )

        error.errors = missing_fields

        raise error

    # -------------------------------------------------
    # IMPORTANT:
    #
    # Do NOT set status to SUBMITTED.
    #
    # Submission immediately enters UNDER_REVIEW.
    # -------------------------------------------------
    submission.status = PropertySubmission.Status.UNDER_REVIEW

    # -------------------------------------------------
    # Keep submitted_at only if the model contains this
    # field. It represents when the owner submitted the
    # property into the review workflow.
    # -------------------------------------------------
    update_fields = [
        "status",
        "updated_at",
    ]

    if hasattr(
        submission,
        "submitted_at",
    ):

        submission.submitted_at = timezone.now()

        update_fields.append(
            "submitted_at",
        )

    submission.save(
        update_fields=update_fields,
    )

    return submission
