from rest_framework.permissions import BasePermission


class CanReviewPropertyVerification(BasePermission):
    """
    Allows access only to users authorized to review
    property verification cases.
    """

    message = (
        "You do not have permission to review property verifications."
    )

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            getattr(user, "is_staff", False)
            or getattr(user, "is_superuser", False)
        )