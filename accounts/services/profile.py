from django.db import transaction

from accounts.models import CustomUser
from accounts.selectors.profile import ProfileSelector


class ProfileService:

    # ==========================================
    # GET COMPLETE PROFILE
    # ==========================================
    @staticmethod
    def get_complete_profile(user):
        profile = ProfileSelector.get_user_profile(user)

        payload = {
            "user": user,
            "profile": profile,
            "profile_completion": ProfileService.calculate_profile_completion(user),
        }

        if user.role == CustomUser.Role.AGENT:
            payload["agent_profile"] = (
                ProfileSelector.get_agent_profile(user)
            )

        elif user.role == CustomUser.Role.LANDLORD:
            payload["landlord_profile"] = (
                ProfileSelector.get_landlord_profile(user)
            )

        return payload

    # ==========================================
    # UPDATE PROFILE
    # ==========================================
    @staticmethod
    @transaction.atomic
    def update_profile(user, validated_data):

        profile = ProfileSelector.get_user_profile(user)

        user.first_name = validated_data.get(
            "first_name",
            user.first_name,
        )

        user.last_name = validated_data.get(
            "last_name",
            user.last_name,
        )

        user.phone_number = validated_data.get(
            "phone_number",
            user.phone_number,
        )

        user.save(
            update_fields=[
                "first_name",
                "last_name",
                "phone_number",
                "updated_at",
            ]
        )

        profile.gender = validated_data.get(
            "gender",
            profile.gender,
        )

        profile.date_of_birth = validated_data.get(
            "date_of_birth",
            profile.date_of_birth,
        )

        profile.bio = validated_data.get(
            "bio",
            profile.bio,
        )

        profile.address = validated_data.get(
            "address",
            profile.address,
        )

        profile.city = validated_data.get(
            "city",
            profile.city,
        )

        profile.state = validated_data.get(
            "state",
            profile.state,
        )

        profile.country = validated_data.get(
            "country",
            profile.country,
        )

        profile.save()

        return ProfileService.get_complete_profile(user)

    # ==========================================
    # UPDATE PROFILE PHOTO
    # ==========================================
    @staticmethod
    def update_profile_photo(user, image):

        profile = ProfileSelector.get_user_profile(user)

        profile.profile_picture = image

        profile.save(
            update_fields=[
                "profile_picture",
                "updated_at",
            ]
        )

        return profile

    # ==========================================
    # PROFILE COMPLETION
    # ==========================================
    @staticmethod
    def calculate_profile_completion(user):

        profile = ProfileSelector.get_user_profile(user)

        score = 0

        checks = [
            user.first_name,
            user.last_name,
            user.email,
            user.phone_number,
            user.is_verified,
            profile.profile_picture,
            profile.gender,
            profile.date_of_birth,
            profile.address,
            profile.city,
            profile.state,
            profile.country,
        ]

        completed = sum(bool(item) for item in checks)

        return round((completed / len(checks)) * 100)