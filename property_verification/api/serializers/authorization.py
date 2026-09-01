from rest_framework import serializers



class PropertyVerificationAuthorizationSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(
        choices=[
            ("authorized", "Authorized"),
            ("rejected", "Rejected"),
        ]
    )

    availability_confirmed = serializers.BooleanField(
        required=False,
        default=False,
    )

    agent_authorized = serializers.BooleanField(
        required=False,
        default=False,
    )

    authorization_note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000,
    )

    rejection_reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000,
    )

    def validate(self, attrs):
        decision = attrs.get("decision")

        availability_confirmed = attrs.get(
            "availability_confirmed",
            False,
        )

        agent_authorized = attrs.get(
            "agent_authorized",
            False,
        )

        rejection_reason = attrs.get(
            "rejection_reason",
            "",
        ).strip()

        # =====================================================
        # AUTHORIZED
        # =====================================================

        if decision == "authorized":

            if not availability_confirmed:
                raise serializers.ValidationError(
                    {
                        "availability_confirmed": (
                            "You must confirm that the "
                            "property is currently available."
                        )
                    }
                )

            if not agent_authorized:
                raise serializers.ValidationError(
                    {
                        "agent_authorized": (
                            "You must confirm that the "
                            "agent is authorized to market "
                            "this property."
                        )
                    }
                )

        # =====================================================
        # REJECTED
        # =====================================================

        elif decision == "rejected":

            if not rejection_reason:
                raise serializers.ValidationError(
                    {
                        "rejection_reason": (
                            "Please provide a reason for " "rejecting this property."
                        )
                    }
                )

        return attrs
