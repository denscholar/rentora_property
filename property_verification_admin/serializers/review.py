from rest_framework import serializers


class PropertyVerificationReviewSerializer(
    serializers.Serializer
):
    """
    Input used by an internal reviewer when making a
    verification decision.
    """

    review_note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=5000,
    )