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

    message = (
        "Only agents, landlords and administrators may "
        "submit properties."
    )

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