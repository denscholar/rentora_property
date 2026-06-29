from django.db import transaction

from accounts.models import CustomUser
from accounts.selectors.profile_selector import (
    get_agent_profile,
    get_landlord_profile,
    get_user_profile,
)


# ==========================================
# GET PROFILE COMPLETION
# ==========================================
def calculate_profile_completion(user):
    """
    Calculates profile completion percentage.

    Total Score = 100
    """

    profile = get_user_profile(user)

    score = 0

    if user.first_name:
        score += 10

    if user.last_name:
        score += 10

    if user.email:
        score += 10

    if user.phone_number:
        score += 10

    if user.is_verified:
        score += 10

    if profile.profile_picture:
        score += 10

    if profile.gender:
        score += 10

    if profile.address:
        score += 10

    if profile.city:
        score += 10

    if profile.state:
        score += 10

    return score


# ==========================================
# GET COMPLETE PROFILE
# ==========================================
def get_complete_profile(user):
    """
    Returns the complete profile payload
    based on the user's role.
    """

    profile = get_user_profile(user)

    payload = {
        "user": user,
        "profile": profile,
        "profile_completion": calculate_profile_completion(user),
    }

    if user.role == CustomUser.Role.AGENT:
        payload["agent_profile"] = get_agent_profile(user)

    elif user.role == CustomUser.Role.LANDLORD:
        payload["landlord_profile"] = get_landlord_profile(user)

    return payload