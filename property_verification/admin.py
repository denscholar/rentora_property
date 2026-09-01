from django.contrib import admin

from property_verification.models.verification import PropertyVerification
from property_verification.models.representative import (
    VerificationRepresentative,
)
from property_verification.models.authorization import (
    PropertyVerificationAuthorization,
)
from property_verification.models.document import (
    PropertyVerificationDocument,
)


@admin.register(PropertyVerification)
class PropertyVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "submission",
        "status",
        "email_status",
        "authorization_sent_at",
        "authorized_at",
        "verified_at",
        "created_at",
    )

    list_filter = (
        "status",
        "email_status",
        "created_at",
        "authorized_at",
        "verified_at",
    )

    search_fields = (
        "submission__id",
        "submission__title",
        "token_hash",
        "email_provider_id",
    )

    readonly_fields = (
        "token_hash",
        "email_sent_at",
        "authorization_sent_at",
        "authorized_at",
        "verified_at",
        "rejected_at",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("reviewed_by",)

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Verification",
            {
                "fields": (
                    "submission",
                    "status",
                    "reviewed_by",
                    "review_note",
                ),
            },
        ),
        (
            "Email",
            {
                "fields": (
                    "email_status",
                    "email_sent_at",
                    "email_provider_id",
                    "email_error",
                ),
            },
        ),
        (
            "Authorization",
            {
                "fields": (
                    "token_hash",
                    "token_expires_at",
                    "authorization_sent_at",
                    "authorized_at",
                ),
            },
        ),
        (
            "Rejection",
            {
                "fields": (
                    "rejected_at",
                    "rejection_reason",
                ),
            },
        ),
        (
            "Verification Completion",
            {
                "fields": ("verified_at",),
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(VerificationRepresentative)
class VerificationRepresentativeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "role",
        "email",
        "phone_number",
        "confirmed_identity",
        "confirmed_authority",
        "verification",
        "created_at",
    )

    list_filter = (
        "role",
        "confirmed_identity",
        "confirmed_authority",
    )

    search_fields = (
        "name",
        "email",
        "phone_number",
        "organization_name",
        "verification__submission__id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


@admin.register(PropertyVerificationAuthorization)
class PropertyVerificationAuthorizationAdmin(admin.ModelAdmin):
    list_display = (
        "verification",
        "decision",
        "availability_confirmed",
        "agent_authorized",
        "responded_at",
    )

    list_filter = (
        "decision",
        "availability_confirmed",
        "agent_authorized",
        "responded_at",
    )

    search_fields = (
        "verification__submission__id",
        "authorization_note",
        "rejection_reason",
        "ip_address",
    )

    readonly_fields = (
        "responded_at",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )

    ordering = ("-responded_at",)

    fieldsets = (
        (
            "Decision",
            {
                "fields": (
                    "verification",
                    "decision",
                    "availability_confirmed",
                    "agent_authorized",
                ),
            },
        ),
        (
            "Notes",
            {
                "fields": (
                    "authorization_note",
                    "rejection_reason",
                ),
            },
        ),
        (
            "Request Metadata",
            {
                "fields": (
                    "responded_at",
                    "ip_address",
                    "user_agent",
                ),
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(PropertyVerificationDocument)
class PropertyVerificationDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "verification",
        "document_type",
        "original_filename",
        "uploaded_by_name",
        "file_size",
        "created_at",
    )

    list_filter = (
        "document_type",
        "created_at",
    )

    search_fields = (
        "public_id",
        "original_filename",
        "uploaded_by_name",
        "verification__submission__id",
    )

    readonly_fields = (
        "public_id",
        "secure_url",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
