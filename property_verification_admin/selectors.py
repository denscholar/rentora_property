from django.db.models import Count

from properties.models.property.submission import PropertySubmission
from property_verification.models import PropertyVerification


def get_admin_verification_queryset():
    return (
        PropertyVerification.objects.select_related(
            "submission",
            "submission__submitted_by",
            "submission__property_type",
            "submission__purpose",
            "submission__area",
            "representative",
            "reviewed_by",
        )
        .annotate(
            documents_count=Count(
                "documents",
                distinct=True,
            )
        )
        .order_by(
            "-created_at",
        )
    )


def get_admin_verification_detail_queryset():
    """
    Queryset optimized for displaying one complete
    verification case to an internal reviewer.
    """

    return PropertyVerification.objects.select_related(
        "submission",
        "submission__submitted_by",
        "submission__property_type",
        "submission__purpose",
        "submission__area",
        "representative",
        "reviewed_by",
    ).prefetch_related(
        "documents",
        "submission__amenities",
        "submission__media",
    )


def get_admin_submission_queryset():
    """
    Queryset used by the property-submission moderation module.
    """

    return (
        PropertySubmission.objects.select_related(
            "submitted_by",
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
            "area",
            "area__lga",
            "area__lga__state",
            "area__lga__state__country",
            "reviewed_by",
            "property_group",
        )
        .prefetch_related(
            "amenities",
            "media",
        )
        .order_by(
            "-created_at",
        )
    )
