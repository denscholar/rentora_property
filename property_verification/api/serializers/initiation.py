from rest_framework import serializers


class InitiatePropertyVerificationSerializer(serializers.Serializer):
    """
    Input used by an agent to identify the landlord's
    authorized representative.
    """

    representative_name = serializers.CharField(
        max_length=255,
        required=True,
    )

    representative_email = serializers.EmailField(
        required=True,
    )

    representative_phone = serializers.CharField(
        max_length=30,
        required=False,
        allow_blank=True,
    )

    representative_role = serializers.ChoiceField(
        choices=[
            ("landlord", "Landlord"),
            ("lawyer", "Lawyer"),
            ("property_manager", "Property Manager"),
            (
                "authorized_representative",
                "Authorized Representative",
            ),
        ],
        required=True,
    )

    organization_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
    )
