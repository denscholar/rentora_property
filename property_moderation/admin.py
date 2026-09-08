from django.contrib import admin

from django.contrib import admin
from .models import (
    PropertyModerationReview,
    PropertyPublication,
)


@admin.register(PropertyModerationReview)
class PropertyModerationReviewAdmin(admin.ModelAdmin):
    list_display = (
        "submission",
        "decision",
        "moderator",
        "reviewed_at",
        "created_at",
    )

    list_filter = (
        "decision",
        "reviewed_at",
        "created_at",
    )

    search_fields = (
        "submission__id",
        "submission__reference",
        "moderator__email",
        "moderator__first_name",
        "moderator__last_name",
        "notes",
        "rejection_reason",
        "information_request",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    raw_id_fields = (
        "submission",
        "moderator",
    )

    ordering = ("-created_at",)

    list_select_related = (
        "submission",
        "moderator",
    )

    fieldsets = (
        (
            "Submission Information",
            {
                "fields": (
                    "id",
                    "submission",
                )
            },
        ),
        (
            "Review Information",
            {
                "fields": (
                    "moderator",
                    "decision",
                    "reviewed_at",
                )
            },
        ),
        (
            "Feedback",
            {
                "fields": (
                    "rejection_reason",
                    "information_request",
                    "notes",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    actions = (
        "mark_approved",
        "mark_rejected",
    )

    @admin.action(description="Mark selected reviews as Approved")
    def mark_approved(self, request, queryset):
        queryset.update(decision=PropertyModerationReview.Decision.APPROVED)

    @admin.action(description="Mark selected reviews as Rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(decision=PropertyModerationReview.Decision.REJECTED)


@admin.register(PropertyPublication)
class PropertyPublicationAdmin(admin.ModelAdmin):
    list_display = (
        "property_group",
        "is_published",
        "published_at",
        "unpublished_at",
        "unpublished_by",
        "created_at",
    )

    list_filter = (
        "is_published",
        "published_at",
        "created_at",
    )

    search_fields = ("property_group__id",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    list_select_related = (
        "property_group",
        "unpublished_by",
    )

    fieldsets = (
        (
            "Publication Information",
            {
                "fields": (
                    "property_group",
                    "is_published",
                )
            },
        ),
        (
            "Publication Dates",
            {
                "fields": (
                    "published_at",
                    "unpublished_at",
                    "unpublished_by",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
