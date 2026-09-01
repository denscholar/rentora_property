# properties/admin/property_submission.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from properties.models.property.submission import PropertySubmission


@admin.register(PropertySubmission)
class PropertySubmissionAdmin(admin.ModelAdmin):
    # =====================================================
    # LIST PAGE
    # =====================================================
    list_display = (
        "id",
        "title",
        "submitted_by",
        "property_type",
        "purpose",
        "area",
        "price_display",
        "status_badge",
        "duplicate_score",
        "created_at",
    )

    list_filter = (
        "status",
        "source",
        "purpose",
        "property_type",
        "property_condition",
        "furnishing_status",
        "is_new_build",
        "is_serviced",
        "is_negotiable",
        "payment_frequency",
        "created_at",
        "reviewed_at",
    )

    search_fields = (
        "title",
        "description",
        "landmark",
        "street_address",
        "submitted_by__email",
        "submitted_by__first_name",
        "submitted_by__last_name",
    )

    ordering = ("-created_at",)

    list_per_page = 50

    date_hierarchy = "created_at"

    autocomplete_fields = (
        "submitted_by",
        "reviewed_by",
        "area",
        "property_type",
        "purpose",
        "property_condition",
        "furnishing_status",
        "amenities",
    )

    filter_horizontal = ("amenities",)

    readonly_fields = (
        "source",
        "status_badge",
        "duplicate_similarity_score",
        "reviewed_by",
        "reviewed_at",
        "created_at",
        "updated_at",
        # "deleted_at",
    )

    save_on_top = True

    actions = (
        "mark_under_review",
        "approve_submissions",
        "reject_submissions",
        "request_more_information",
    )

    # =====================================================
    # FIELDSETS
    # =====================================================

    fieldsets = (
        (
            "Submission Information",
            {
                "fields": (
                    "submitted_by",
                    "source",
                    "status",
                    "status_badge",
                )
            },
        ),
        (
            "Property Details",
            {
                "fields": (
                    "title",
                    "description",
                    "property_type",
                    "purpose",
                    "property_condition",
                    "furnishing_status",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "area",
                    "street_address",
                    "landmark",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            "Property Features",
            {
                "fields": (
                    "bedrooms",
                    "bathrooms",
                    "toilets",
                    "parking_spaces",
                    "floors",
                    "units_available",
                    "year_built",
                    "amenities",
                )
            },
        ),
        (
            "Size Information",
            {
                "fields": (
                    "size_unit",
                    "land_size",
                    "building_size",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "proposed_price",
                    "payment_frequency",
                    "service_charge",
                    "agency_fee",
                    "legal_fee",
                    "caution_fee",
                )
            },
        ),
        (
            "Availability",
            {
                "fields": (
                    "available_from",
                    "minimum_stay",
                    "is_new_build",
                    "is_serviced",
                    "is_negotiable",
                )
            },
        ),
        (
            "Review Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "duplicate_similarity_score",
                    "review_note",
                    "reviewed_by",
                    "reviewed_at",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                    # "deleted_at",
                ),
            },
        ),
    )

    # =====================================================
    # QUERY OPTIMIZATION
    # =====================================================

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.select_related(
            "submitted_by",
            "reviewed_by",
            "area",
            "property_type",
            "purpose",
            "property_condition",
            "furnishing_status",
        ).prefetch_related("amenities")

    # =====================================================
    # DISPLAY HELPERS
    # =====================================================

    @admin.display(description="Price")
    def price_display(self, obj):
        if not obj.proposed_price:
            return "-"
        return f"₦{obj.proposed_price:,.2f}"

    @admin.display(description="Duplicate %")
    def duplicate_score(self, obj):
        if obj.duplicate_similarity_score is None:
            return "-"
        return f"{obj.duplicate_similarity_score}%"

    @admin.display(description="Status")
    def status_badge(self, obj):

        colors = {
            PropertySubmission.Status.DRAFT: "#6c757d",
            PropertySubmission.Status.UNDER_REVIEW: "#0d6efd",
            PropertySubmission.Status.APPROVED: "#198754",
            PropertySubmission.Status.REJECTED: "#dc3545",
            # PropertySubmission.Status.DUPLICATE_FOUND: "#fd7e14",
            # PropertySubmission.Status.MORE_INFORMATION_REQUIRED: "#ffc107",
        }

        color = colors.get(obj.status, "#6c757d")

        return format_html(
            """
            <span style="
                background:{};
                color:white;
                padding:4px 10px;
                border-radius:12px;
                font-weight:600;
            ">
                {}
            </span>
            """,
            color,
            obj.get_status_display(),
        )

    # =====================================================
    # BULK ACTIONS
    # =====================================================

    @admin.action(description="Move selected to Under Review")
    def mark_under_review(self, request, queryset):
        queryset.update(status=PropertySubmission.Status.UNDER_REVIEW)

    @admin.action(description="Approve selected submissions")
    def approve_submissions(self, request, queryset):
        queryset.update(
            status=PropertySubmission.Status.APPROVED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Reject selected submissions")
    def reject_submissions(self, request, queryset):
        queryset.update(
            status=PropertySubmission.Status.REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )

    @admin.action(description="Request more information")
    def request_more_information(self, request, queryset):
        queryset.update(
            status=PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )


def changelist_view(self, request, extra_context=None):

    extra_context = extra_context or {}

    extra_context["pending_count"] = PropertySubmission.objects.filter(
        status=PropertySubmission.Status.UNDER_REVIEW
    ).count()

    return super().changelist_view(
        request,
        extra_context=extra_context,
    )


# 2. Highlight High Duplicate Scores
@admin.display(description="Duplicate")
def duplicate_score(self, obj):

    value = obj.duplicate_similarity_score

    if value is None:
        return "-"

    color = "green"

    if value >= 80:
        color = "red"
    elif value >= 50:
        color = "orange"

    return format_html(
        '<strong style="color:{};">{}%</strong>',
        color,
        value,
    )


# 3. Restrict Editing After Approval
def get_readonly_fields(self, request, obj=None):

    readonly = list(self.readonly_fields)

    if obj and obj.status == PropertySubmission.Status.APPROVED:
        readonly.extend([f.name for f in obj._meta.fields])

    return readonly
