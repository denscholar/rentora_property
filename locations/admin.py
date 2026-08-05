from django.contrib import admin

from .models import Country, State, LGA, Area


# =====================================================
# COUNTRY ADMIN
# =====================================================
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "display_order",
        "created_at",
    )
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("display_order", "name")


# =====================================================
# STATE ADMIN
# =====================================================
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "is_active",
        "display_order",
        "created_at",
    )
    search_fields = ("name", "country__name")
    list_filter = ("country", "is_active")
    ordering = ("display_order", "name")


# =====================================================
# LGA ADMIN
# =====================================================
@admin.register(LGA)
class LGAAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "state",
        "is_active",
        "display_order",
        "created_at",
    )
    search_fields = ("name", "state__name")
    list_filter = ("state", "is_active")
    ordering = ("display_order", "name")


# =====================================================
# AREA ADMIN
# =====================================================
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "lga",
        "latitude",
        "longitude",
        "is_active",
        "display_order",
        "created_at",
    )
    search_fields = (
        "name",
        "lga__name",
        "lga__state__name",
    )
    list_filter = (
        "lga",
        "is_active",
    )
    ordering = ("display_order", "name")