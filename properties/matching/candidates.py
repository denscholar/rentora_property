"""
Candidate generation for the property duplicate matching engine.

This module does NOT determine whether two properties are
duplicates.

Its responsibility is only to produce a safe and reasonably
small set of existing submissions that are worth comparing
against a new submission.
"""

from django.db.models import QuerySet

from properties.models import PropertySubmission

from properties.matching.category import (
    resolve_property_category,
)


# ============================================================
# MATCHABLE STATUSES
# ============================================================

"""
These are the statuses that should participate in duplicate
matching.

A draft is included because an agent may create the same
property through another submission while the original is
still incomplete.

Under review is included because this is one of the most
important points at which duplicate detection should happen.

Approved is included because another agent may subsequently
submit the same physical property.

Rejected and duplicate_found are intentionally excluded from
the normal candidate pool.

more_information_required remains matchable because the
property may still become a valid submission after the agent
provides the missing information.
"""

MATCHABLE_STATUSES = (
    PropertySubmission.Status.DRAFT,
    PropertySubmission.Status.UNDER_REVIEW,
    PropertySubmission.Status.APPROVED,
    PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
)


# ============================================================
# CANDIDATE GENERATOR
# ============================================================

def get_duplicate_candidates(
    *,
    submission: PropertySubmission,
) -> QuerySet:
    """
    Return existing PropertySubmission records that are
    reasonable duplicate candidates for `submission`.

    IMPORTANT:

    This function does NOT calculate a duplicate score.

    It only performs the first safe narrowing of the search
    space.
    """

    # --------------------------------------------------------
    # Resolve the new submission's category.
    # --------------------------------------------------------

    category = resolve_property_category(
        submission.property_type,
    )

    # --------------------------------------------------------
    # Start with submissions belonging to the same user-facing
    # property category.
    #
    # Since category is derived from PropertyType rather than
    # stored directly on PropertySubmission, we first determine
    # which PropertyType records belong to the same category.
    # --------------------------------------------------------

    property_type_ids = _get_property_type_ids_for_category(
        category=category,
    )

    queryset = (
        PropertySubmission.objects
        .select_related(
            "property_type",
            "purpose",
            "area",
            "area__lga",
        )
        .filter(
            property_type_id__in=property_type_ids,
            status__in=MATCHABLE_STATUSES,
            is_archived=False
        )
        .exclude(
            pk=submission.pk,
        )
    )

    # --------------------------------------------------------
    # Same purpose
    # --------------------------------------------------------

    if submission.purpose_id:
        queryset = queryset.filter(
            purpose_id=submission.purpose_id,
        )

    # --------------------------------------------------------
    # Same area
    # --------------------------------------------------------

    if submission.area_id:
        queryset = queryset.filter(
            area_id=submission.area_id,
        )

    # --------------------------------------------------------
    # Never compare archived submissions.
    #
    # SoftArchiveMixin is expected to expose `is_archived`.
    # If your mixin uses a different field name, we'll adjust
    # this one line.
    # --------------------------------------------------------

    queryset = queryset.filter(
        is_archived=False,
    )

    return queryset.order_by(
        "-created_at",
    )


# ============================================================
# PROPERTY TYPES FOR CATEGORY
# ============================================================

def _get_property_type_ids_for_category(
    *,
    category: str,
) -> list[int]:
    """
    Return PropertyType primary keys that belong to the
    supplied matching category.
    """

    from properties.models.lookups import PropertyType

    property_types = PropertyType.objects.all()

    matching_ids = []

    for property_type in property_types:

        try:
            resolved_category = resolve_property_category(
                property_type,
            )

        except ValueError:
            # Unknown lookup types are not allowed to silently
            # become duplicate candidates.
            continue

        if resolved_category == category:
            matching_ids.append(
                property_type.pk,
            )

    return matching_ids