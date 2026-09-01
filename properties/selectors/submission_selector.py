from django.db.models import QuerySet
from django.db.models import Q
from properties.models import PropertySubmission


def get_submission_queryset() -> QuerySet:
    """
    Returns an optimized base queryset for property submissions.
    """

    return PropertySubmission.objects.select_related(
        "submitted_by",
        "property_type",
        "purpose",
        "property_condition",
        "furnishing_status",
        "area",
        "area__lga",
        "area__lga__state",
        "area__lga__state__country",
    ).prefetch_related(
        "amenities",
        "amenities__category",
    )


# =====================================================
# USER SUBMISSION QUERYSET
# =====================================================
def get_user_submissions(
    *,
    user,
    status=None,
    search=None,
) -> QuerySet[PropertySubmission]:
    """
    Returns every non-archived submission belonging to a user.

    Ordered by newest first.
    """

    queryset = (
        PropertySubmission.objects.filter(
            submitted_by=user,
            is_archived=False,
        )
        .select_related(
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
            "area",
            "submitted_by",
        )
        .prefetch_related(
            "amenities",
        )
        .order_by("-created_at")
    )


# ---------------------------------------------------------
    # STATUS FILTER
    # ---------------------------------------------------------
    #
    # The frontend only exposes these workflow states:
    #
    #   draft
    #   under_review
    #   approved
    #   rejected
    #
    # MORE_INFORMATION_REQUIRED is also a valid backend state,
    # but it is intentionally not represented as a separate UI
    # filter because it belongs to the editable workflow.
    #
    if status:
        queryset = queryset.filter(status=status)

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    #
    # Search across useful property-submission fields.
    #
    if search:
        search = search.strip()

        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(street_address__icontains=search)
            | Q(landmark__icontains=search)
            | Q(property_type__name__icontains=search)
            | Q(area__name__icontains=search)
        )

    return queryset

# =====================================================
# USER SUBMISSION
# =====================================================
def get_user_submission(
    *,
    uuid,
    user,
) -> PropertySubmission:
    """
    Returns one submission belonging to a user.
    """

    return (
        PropertySubmission.objects.select_related(
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
            "area",
            "submitted_by",
        )
        .prefetch_related(
            "amenities",
        )
        .get(
            uuid=uuid,
            submitted_by=user,
            is_archived=False,
        )
    )


# =====================================================
# REVIEW QUEUE
# =====================================================
def get_review_queue():
    """
    Returns every submission awaiting review.
    """

    return (
        PropertySubmission.objects.filter(
            status=PropertySubmission.Status.UNDER_REVIEW,
            is_archived=False,
        )
        .select_related(
            "submitted_by",
            "property_type",
            "purpose",
            "area",
        )
        .order_by(
            "created_at",
        )
    )


# =====================================================
# POSSIBLE DUPLICATES
# =====================================================
def get_possible_duplicate_submissions(
    *,
    area,
    property_type,
    bedrooms,
):
    """
    Returns submissions that may describe the same property.
    """

    return PropertySubmission.objects.filter(
        area=area,
        property_type=property_type,
        bedrooms=bedrooms,
        is_archived=False,
    )


# =====================================================
# SUBMISSION COUNT
# =====================================================
def get_submission_count(
    *,
    user,
):
    """
    Returns the number of active submissions.
    """

    return PropertySubmission.objects.filter(
        submitted_by=user,
        is_archived=False,
    ).count()


# =====================================================
# STATUS COUNT
# =====================================================
def get_submission_status_counts(
    *,
    user,
):
    """
    Returns submission counts grouped by status.
    """

    queryset = get_user_submissions(
        user=user,
    )

    return {
        "draft": queryset.filter(
            status=PropertySubmission.Status.DRAFT,
        ).count(),
        "under_review": queryset.filter(
            status=PropertySubmission.Status.UNDER_REVIEW,
        ).count(),
        "approved": queryset.filter(
            status=PropertySubmission.Status.APPROVED,
        ).count(),
        "rejected": queryset.filter(
            status=PropertySubmission.Status.REJECTED,
        ).count(),
    }
