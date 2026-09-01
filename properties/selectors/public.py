from properties.models import PropertySubmission
from property_verification.models import PropertyVerification


def get_public_property_queryset():
    """
    Returns only properties that are eligible for public discovery.

    Public visibility requires:

        PropertySubmission.status == APPROVED
        PropertyVerification.status == VERIFIED
        PropertySubmission.is_archived == False
    """

    return (
        PropertySubmission.objects
        .filter(
            status=PropertySubmission.Status.APPROVED,
            is_archived=False,
            verification__status=(
                PropertyVerification.VerificationStatus.VERIFIED
            ),
        )
        .select_related(
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
            "area",
            "area__lga",
            "area__lga__state",
            "area__lga__state__country",
        )
        .prefetch_related(
            "amenities",
            "media",
        )
        .order_by(
            "-created_at",
        )
    )