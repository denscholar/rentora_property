from rest_framework import serializers

from properties.models.property.submission import PropertySubmission
from property_verification.models import (
    PropertyVerification,
    VerificationRepresentative,
)


class PublicPropertyVerificationSerializer(serializers.ModelSerializer):
    property = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    representative = serializers.SerializerMethodField()

    class Meta:
        model = PropertyVerification
        fields = [
            "uuid",
            "status",
            "token_expires_at",
            "property",
            "agent",
            "representative",
        ]

    def get_property(self, obj):
        submission = obj.submission

        return {
            "uuid": str(submission.uuid),
            "title": submission.title,
            "property_type": (
                str(submission.property_type) if submission.property_type else None
            ),
            "purpose": (str(submission.purpose) if submission.purpose else None),
            "area": (str(submission.area) if submission.area else None),
            "street_address": submission.street_address,
            "bedrooms": submission.bedrooms,
            "bathrooms": submission.bathrooms,
        }

    def get_agent(self, obj):
        agent = obj.submission.submitted_by

        return {
            "name": (f"{agent.first_name} " f"{agent.last_name}").strip(),
            "email": agent.email,
        }

    def get_representative(self, obj):
        representative = getattr(obj, "representative", None)

        if not representative:
            return None

        return {
            "name": representative.name,
            "role": representative.get_role_display(),
            "email": representative.email,
            "phone_number": representative.phone_number,
            "organization_name": representative.organization_name,
        }
