from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, AgentProfile, LandlordProfile


# ==========================================
# CUSTOM USER ADMIN
# ==========================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "id",
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "role",
        "is_verified",
        "is_active",
        "is_staff",
        "created_at",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_active",
        "is_staff",
        "created_at",
    )

    search_fields = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "slug",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Login Details",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "is_verified",
                    "email_verified_at",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
        "last_login",
        "date_joined",
    )

    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# ==========================================
# USER PROFILE ADMIN
# ==========================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "gender",
        "city",
        "state",
        "created_at",
    )
    list_filter = (
        "gender",
        "city",
        "state",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ==========================================
# AGENT PROFILE ADMIN
# ==========================================
@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "agency_name",
        "verification_status",
        "rating_average",
        "completed_viewings",
        "cancelled_viewings",
        "no_show_count",
        "created_at",
    )
    list_filter = (
        "verification_status",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "agency_name",
    )
    readonly_fields = (
        "rating_average",
        "completed_viewings",
        "cancelled_viewings",
        "no_show_count",
        "created_at",
        "updated_at",
    )


# ==========================================
# LANDLORD PROFILE ADMIN
# ==========================================
@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "landlord_type",
        "business_name",
        "verification_status",
        "total_properties",
        "created_at",
    )
    list_filter = (
        "landlord_type",
        "verification_status",
        "created_at",
    )
    search_fields = (
        "user__email",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "business_name",
    )
    readonly_fields = (
        "total_properties",
        "created_at",
        "updated_at",
    )
