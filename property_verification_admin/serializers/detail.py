from rest_framework import serializers

from properties.api.serializers.submission.media import (
    PropertySubmissionMediaSerializer,
)
from properties.models.property.submission import PropertySubmission
from property_verification.models import PropertyVerification


class PropertyVerificationAdminDetailSerializer(serializers.ModelSerializer):
    property = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    representative = serializers.SerializerMethodField()
    authorization = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    class Meta:
        model = PropertyVerification
        fields = [
            "uuid",
            "status",
            "token_expires_at",
            "authorization_sent_at",
            "authorized_at",
            "verified_at",
            "rejected_at",
            "rejection_reason",
            "review_note",
            "reviewed_by_name",
            "property",
            "agent",
            "media",
            "representative",
            "authorization",
            "documents",
            "created_at",
            "updated_at",
        ]

    def get_property(self, obj):
        submission = obj.submission

        property_type = submission.property_type
        purpose = submission.purpose
        area = submission.area

        return {
            "uuid": str(submission.uuid),
            "title": submission.title,
            "description": submission.description,
            "property_type": (
                {
                    "uuid": str(property_type.uuid),
                    "name": property_type.name,
                    "code": property_type.code,
                }
                if property_type
                else None
            ),
            "purpose": (
                {
                    "uuid": str(purpose.uuid),
                    "name": purpose.name,
                    "code": purpose.code,
                }
                if purpose
                else None
            ),
            "area": (
                {
                    "uuid": str(area.uuid),
                    "name": area.name,
                }
                if area
                else None
            ),
            "street_address": submission.street_address,
            "landmark": submission.landmark,
            "bedrooms": submission.bedrooms,
            "bathrooms": submission.bathrooms,
            "toilets": submission.toilets,
            "parking_spaces": submission.parking_spaces,
            "floors": submission.floors,
            "units_available": submission.units_available,
            "year_built": submission.year_built,
            "is_new_build": submission.is_new_build,
            "is_serviced": submission.is_serviced,
            "is_negotiable": submission.is_negotiable,
            "land_size": submission.land_size,
            "building_size": submission.building_size,
            "size_unit": submission.size_unit,
            "payment_frequency": submission.payment_frequency,
            "proposed_price": submission.proposed_price,
            "service_charge": submission.service_charge,
            "caution_fee": submission.caution_fee,
            "legal_fee": submission.legal_fee,
            "agency_fee": submission.agency_fee,
            "latitude": submission.latitude,
            "longitude": submission.longitude,
            "submission_status": submission.status,
            "submission_status_display": (submission.get_status_display()),
        }

    def get_agent(self, obj):
        agent = obj.submission.submitted_by

        full_name_method = getattr(
            agent,
            "get_full_name",
            None,
        )

        if callable(full_name_method):
            name = full_name_method()
        else:
            name = (
                f"{getattr(agent, 'first_name', '')} "
                f"{getattr(agent, 'last_name', '')}"
            ).strip()

        return {
            "uuid": str(agent.slug),
            "name": name or getattr(agent, "email", ""),
            "email": getattr(agent, "email", ""),
            "phone_number": getattr(
                agent,
                "phone_number",
                "",
            ),
        }

    def get_representative(self, obj):
        representative = getattr(
            obj,
            "representative",
            None,
        )

        if representative is None:
            return None

        return {
            "uuid": str(representative.uuid),
            "name": representative.name,
            "role": representative.role,
            "role_display": representative.get_role_display(),
            "email": representative.email,
            "phone_number": representative.phone_number,
            "organization_name": representative.organization_name,
            "confirmed_identity": representative.confirmed_identity,
            "confirmed_authority": representative.confirmed_authority,
        }

    def get_authorization(self, obj):
        authorization = getattr(
            obj,
            "authorization",
            None,
        )

        if authorization is None:
            return None

        return {
            "uuid": str(authorization.uuid),
            "decision": authorization.decision,
            "availability_confirmed": (authorization.availability_confirmed),
            "agent_authorized": (authorization.agent_authorized),
            "authorization_note": (authorization.authorization_note),
            "responded_at": authorization.responded_at,
            "ip_address": (
                str(authorization.ip_address) if authorization.ip_address else None
            ),
            "user_agent": authorization.user_agent,
        }

    def get_documents(self, obj):
        documents = obj.documents.all()

        return [
            {
                "uuid": str(document.uuid),
                "document_type": document.document_type,
                "document_type_display": (document.get_document_type_display()),
                "original_filename": (document.original_filename),
                "secure_url": document.secure_url,
                "content_type": document.content_type,
                "file_size": document.file_size,
                "uploaded_by_name": (document.uploaded_by_name),
                "created_at": document.created_at,
            }
            for document in documents
        ]

    def get_reviewed_by_name(self, obj):
        reviewer = obj.reviewed_by

        if reviewer is None:
            return None

        full_name_method = getattr(
            reviewer,
            "get_full_name",
            None,
        )

        if callable(full_name_method):
            full_name = full_name_method()

            if full_name:
                return full_name

        return (
            f"{getattr(reviewer, 'first_name', '')} "
            f"{getattr(reviewer, 'last_name', '')}"
        ).strip() or getattr(
            reviewer,
            "email",
            "",
        )

    def get_media(self, obj):
        submission = obj.submission

        return PropertySubmissionMediaSerializer(
            submission.media.all(),
            many=True,
            context=self.context,
        ).data
