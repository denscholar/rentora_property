from django.contrib import admin

from properties.models import (
    Amenity,
    AmenityCategory,
    PropertyPurpose,
    PropertyType,
)

from properties.models import FurnishingStatus, PropertyCondition


# =====================================================
# PROPERTY TYPE ADMIN
# =====================================================
@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "icon",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "uuid",
        "slug",
        "created_at",
        "updated_at",
    )


# =====================================================
# PROPERTY PURPOSE ADMIN
# =====================================================
@admin.register(PropertyPurpose)
class PropertyPurposeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "allow_viewing_booking",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "allow_viewing_booking",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "uuid",
        "slug",
        "created_at",
        "updated_at",
    )


# =====================================================
# AMENITY CATEGORY ADMIN
# =====================================================
@admin.register(AmenityCategory)
class AmenityCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "uuid",
        "slug",
        "created_at",
        "updated_at",
    )


# =====================================================
# AMENITY ADMIN
# =====================================================
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "icon",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "category__name",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "uuid",
        "slug",
        "created_at",
        "updated_at",
    )


# =====================================================
# PROPERTY CONDITION ADMIN
# =====================================================
@admin.register(PropertyCondition)
class PropertyConditionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "uuid",
        "slug",
        "created_at",
        "updated_at",
    )


# =====================================================
# FURNISHING STATUS ADMIN
# =====================================================
@admin.register(FurnishingStatus)
class FurnishingStatusAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )

    ordering = (
        "display_order",
        "name",
    )

    readonly_fields = (
        "uuid",
        "slug",
        "created_at",
        "updated_at",
    )
