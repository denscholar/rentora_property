from rest_framework import serializers

from property_verification.models import (
    PropertyVerification,
    PropertyVerificationDocument,
    VerificationDocumentType,
)
from property_verification.validators import (
    validate_property_verification_document,
)


class PropertyVerificationDocumentUploadSerializer(serializers.Serializer):
    """
    Serializer used by the public property verification
    document upload endpoint.

    The actual file is uploaded to Cloudinary by the service.
    """

    document_type = serializers.ChoiceField(
        choices=VerificationDocumentType.choices,
    )

    document = serializers.FileField(
        validators=[
            validate_property_verification_document,
        ],
    )


class PropertyVerificationDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer used to return a saved verification document.
    """

    document_type_display = serializers.CharField(
        source="get_document_type_display",
        read_only=True,
    )

    class Meta:
        model = PropertyVerificationDocument

        fields = [
            "uuid",
            "document_type",
            "document_type_display",
            "secure_url",
            "original_filename",
            "content_type",
            "file_size",
            "uploaded_by_name",
            "created_at",
        ]

        read_only_fields = [
            "uuid",
            "document_type_display",
            "secure_url",
            "original_filename",
            "content_type",
            "file_size",
            "uploaded_by_name",
            "created_at",
        ]
