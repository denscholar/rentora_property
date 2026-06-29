from django.shortcuts import get_object_or_404

from accounts.models import (
    AgentProfile,
    LandlordProfile,
    UserProfile,
)


# ==========================================
# GET USER PROFILE
# ==========================================
def get_user_profile(user):
    return get_object_or_404(
        UserProfile,
        user=user,
    )


# ==========================================
# GET AGENT PROFILE
# ==========================================
def get_agent_profile(user):
    return AgentProfile.objects.filter(
        user=user,
    ).first()


# ==========================================
# GET LANDLORD PROFILE
# ==========================================
def get_landlord_profile(user):
    return LandlordProfile.objects.filter(
        user=user,
    ).first()