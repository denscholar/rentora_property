from django.shortcuts import get_object_or_404

from accounts.models import (
    AgentProfile,
    LandlordProfile,
    UserProfile,
)


# =====================================================
# PROFILE SELECTOR
# =====================================================

class ProfileSelector:

    @staticmethod
    def get_user_profile(user):
        return get_object_or_404(
            UserProfile,
            user=user,
        )

    @staticmethod
    def get_agent_profile(user):
        return AgentProfile.objects.filter(
            user=user,
        ).first()

    @staticmethod
    def get_landlord_profile(user):
        return LandlordProfile.objects.filter(
            user=user,
        ).first()