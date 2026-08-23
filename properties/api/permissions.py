from rest_framework.permissions import BasePermission

from accounts.models import CustomUser


# =====================================================
# CAN SUBMIT PROPERTY
# =====================================================
class CanSubmitProperty(BasePermission):
    """
    Allows agents, landlords and administrators to manage property
    submissions.

    Tenants cannot create or manage property submissions.
    """

    message = "Only agents, landlords and administrators may " "submit properties."

    allowed_roles = {
        CustomUser.Role.AGENT,
        CustomUser.Role.LANDLORD,
        CustomUser.Role.ADMIN,
    }

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.is_verified
            and user.role in self.allowed_roles
        )


# =====================================================
# CAN MODERATE PROPERTIES
# =====================================================


class IsPropertyModerator(BasePermission):

    message = (
        "You do not have permission to perform "
        "this property moderation action."
    )

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        permission_code = getattr(
            view,
            "permission_code",
            None,
        )

        if not permission_code:
            return False

        return user.has_admin_permission(
            permission_code
        )