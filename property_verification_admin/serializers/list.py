from rest_framework import serializers

from property_verification.models import PropertyVerification


class PropertyVerificationAdminListSerializer(serializers.ModelSerializer):
    submission_uuid = serializers.UUIDField(
        source="submission.uuid",
        read_only=True,
    )

    property_title = serializers.CharField(
        source="submission.title",
        read_only=True,
    )

    property_type = serializers.CharField(
        source="submission.property_type.name",
        read_only=True,
    )

    purpose = serializers.CharField(
        source="submission.purpose.name",
        read_only=True,
    )

    area = serializers.CharField(
        source="submission.area.name",
        read_only=True,
    )

    submitted_by_name = serializers.SerializerMethodField()

    representative_name = serializers.CharField(
        source="representative.name",
        read_only=True,
    )

    representative_role = serializers.CharField(
        source="representative.role",
        read_only=True,
    )

    documents_count = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = PropertyVerification

        fields = [
            "uuid",
            "submission_uuid",
            "property_title",
            "property_type",
            "purpose",
            "area",
            "submitted_by_name",
            "representative_name",
            "representative_role",
            "status",
            "token_expires_at",
            "authorization_sent_at",
            "authorized_at",
            "documents_count",
            "created_at",
            "updated_at",
        ]

    def get_submitted_by_name(self, obj):
        user = obj.submission.submitted_by

        get_full_name = getattr(
            user,
            "get_full_name",
            None,
        )

        if callable(get_full_name):
            full_name = get_full_name()

            if full_name:
                return full_name

        return (
            f"{getattr(user, 'first_name', '')} " f"{getattr(user, 'last_name', '')}"
        ).strip() or getattr(
            user,
            "email",
            "",
        )
