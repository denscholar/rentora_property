from rest_framework import serializers

from accounts.models import AgentProfile, CustomUser, LandlordProfile, UserProfile


# ==========================================
# REGISTER SERIALIZER
# ==========================================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "password",
            "confirm_password",
        ]

    def validate_role(self, value):
        if value == CustomUser.Role.ADMIN:
            raise serializers.ValidationError("You cannot register as an admin.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        return attrs


# ==========================================
# VERIFY EMAIL OTP SERIALIZER
# ==========================================
class VerifyEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)


# ==========================================
# RESEND EMAIL OTP SERIALIZER
# ==========================================
class ResendEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


# ==========================================
# LOGIN SERIALIZER
# ==========================================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# ==========================================
# LOGGED IN USER SERIALIZER
# ==========================================
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "slug",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_verified",
        ]



# =====================================================
# AUTH USER SERIALIZER
# =====================================================
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "slug",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_verified",
        ]


# =====================================================
# USER PROFILE SERIALIZER
# =====================================================
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "date_of_birth",
            "gender",
            "bio",
            "address",
            "city",
            "state",
            "country",
        ]


# =====================================================
# AGENT PROFILE SERIALIZER
# =====================================================
class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = [
            "agency_name",
            "business_address",
            "years_of_experience",
            "verification_status",
            "rating_average",
            "completed_viewings",
            "cancelled_viewings",
            "no_show_count",
        ]


# =====================================================
# LANDLORD PROFILE SERIALIZER
# =====================================================
class LandlordProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = [
            "landlord_type",
            "business_name",
            "verification_status",
            "total_properties",
        ]


# =====================================================
# UPDATE PROFILE SERIALIZER
# =====================================================
class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    bio = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)


# =====================================================
# PROFILE PHOTO SERIALIZER
# =====================================================
class ProfilePhotoSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()