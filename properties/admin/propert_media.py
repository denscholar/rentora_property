from django.contrib import admin

from django.contrib import admin
from django.utils.html import format_html

from properties.models.property.media import PropertySubmissionMedia


class PropertySubmissionMediaInline(admin.TabularInline):
    model = PropertySubmissionMedia
    extra = 0

    fields = (
        "display_order",
        "media_type",
        "preview",
        "is_cover",
        "upload_status",
    )

    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.secure_url and obj.is_image:
            return format_html(
                "{}",
                obj.secure_url,
            )

        return "-"


@admin.register(PropertySubmissionMedia)
class PropertySubmissionMediaAdmin(admin.ModelAdmin):
    inline = PropertySubmissionMediaInline

    list_display = (
        "id",
        "preview",
        "submission",
        "media_type_badge",
        "original_filename",
        "upload_status_badge",
        "is_cover",
        "display_order",
        "file_size_display",
        "created_at",
    )

    list_filter = (
        "media_type",
        "upload_status",
        "is_cover",
        "created_at",
    )

    search_fields = (
        "public_id",
        "asset_id",
        "original_filename",
        "caption",
        "submission__id",
    )

    ordering = (
        "submission",
        "display_order",
        "-created_at",
    )

    list_select_related = ("submission",)

    readonly_fields = (
        "preview_large",
        "public_id",
        "asset_id",
        "secure_url",
        "resource_type",
        "file_format",
        "content_type",
        "file_size",
        "width",
        "height",
        "duration",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("submission",)

    list_per_page = 50

    fieldsets = (
        (
            "Relationship",
            {"fields": ("submission",)},
        ),
        (
            "Preview",
            {"fields": ("preview_large",)},
        ),
        (
            "Media Information",
            {
                "fields": (
                    "media_type",
                    "upload_status",
                    "original_filename",
                    "caption",
                    "alt_text",
                    "is_cover",
                    "display_order",
                )
            },
        ),
        (
            "Cloudinary Metadata",
            {
                "classes": ("collapse",),
                "fields": (
                    "public_id",
                    "asset_id",
                    "secure_url",
                    "resource_type",
                    "file_format",
                    "content_type",
                    "file_size",
                    "width",
                    "height",
                    "duration",
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
                ),
            },
        ),
    )

    actions = (
        "mark_completed",
        "mark_failed",
        "make_cover_image",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("submission")

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.media_type == obj.MediaType.IMAGE and obj.secure_url:
            return format_html(
                """
                {}
                """,
                obj.secure_url,
            )

        if obj.media_type == obj.MediaType.VIDEO:
            return "🎥 Video"

        return "-"

    @admin.display(description="Media Preview")
    def preview_large(self, obj):
        if not obj.pk:
            return "Save object first."

        if obj.media_type == obj.MediaType.IMAGE and obj.secure_url:
            return format_html(
                """
                {}
                """,
                obj.secure_url,
            )

        if obj.media_type == obj.MediaType.VIDEO and obj.secure_url:
            return format_html(
                """
                <video
                    width="500"
                    controls
                    style="border-radius:12px;"
                >
                    {}
                    Your browser does not support video playback.
                </video>
                """,
                obj.secure_url,
            )

        return "-"

    @admin.display(
        description="Type",
        ordering="media_type",
    )
    def media_type_badge(self, obj):
        colors = {
            "image": "#198754",
            "video": "#0d6efd",
        }

        return format_html(
            """
            <span
                style="
                    background:{};
                    color:white;
                    padding:4px 10px;
                    border-radius:6px;
                    font-weight:600;
                "
            >
                {}
            </span>
            """,
            colors.get(obj.media_type, "#6c757d"),
            obj.get_media_type_display(),
        )

    @admin.display(
        description="Status",
        ordering="upload_status",
    )
    def upload_status_badge(self, obj):
        colors = {
            "completed": "#198754",
            "pending": "#ffc107",
            "failed": "#dc3545",
        }

        return format_html(
            """
            <span
                style="
                    background:{};
                    color:white;
                    padding:4px 10px;
                    border-radius:6px;
                    font-weight:600;
                "
            >
                {}
            </span>
            """,
            colors.get(obj.upload_status, "#6c757d"),
            obj.get_upload_status_display(),
        )

    @admin.display(description="File Size")
    def file_size_display(self, obj):
        if not obj.file_size:
            return "-"

        size = float(obj.file_size)

        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024

        return f"{size:.1f} PB"

    @admin.action(description="Mark selected media as Completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(
            upload_status=PropertySubmissionMedia.UploadStatus.COMPLETED
        )

        self.message_user(
            request,
            f"{updated} media file(s) marked as completed.",
        )

    @admin.action(description="Mark selected media as Failed")
    def mark_failed(self, request, queryset):
        updated = queryset.update(
            upload_status=PropertySubmissionMedia.UploadStatus.FAILED
        )

        self.message_user(
            request,
            f"{updated} media file(s) marked as failed.",
        )

    @admin.action(description="Set selected image(s) as cover image")
    def make_cover_image(self, request, queryset):
        updated = 0

        for media in queryset:
            if media.media_type != media.MediaType.IMAGE:
                continue

            PropertySubmissionMedia.objects.filter(
                submission=media.submission,
                is_cover=True,
            ).update(is_cover=False)

            media.is_cover = True
            media.save(update_fields=["is_cover"])

            updated += 1

        self.message_user(
            request,
            f"{updated} image(s) set as cover image.",
        )
