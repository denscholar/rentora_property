from rest_framework import serializers


class PropertySubmissionReviewSerializer(
    serializers.Serializer
):
    """
    Input used by SheltaMe staff when approving
    or rejecting a property submission.
    """

    review_note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=5000,
    )