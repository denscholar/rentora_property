from rest_framework import serializers

from accounts.models import AgentProfile, CustomUser, LandlordProfile, UserProfile
from accounts.utils.phone_numbers import normalize_phone_number

# ==========================================
# REGISTER SERIALIZER
# ==========================================
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)
#     confirm_password = serializers.CharField(write_only=True, min_length=8)

#     class Meta:
#         model = CustomUser
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "phone_number",
#             "role",
#             "password",
#             "confirm_password",
#         ]

#     def validate_role(self, value):
#         if value == CustomUser.Role.ADMIN:
#             raise serializers.ValidationError("You cannot register as an admin.")
#         return value

#     def validate(self, attrs):
#         if attrs["password"] != attrs["confirm_password"]:
#             raise serializers.ValidationError(
#                 {"confirm_password": "Passwords do not match."}
#             )

#         return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    phone_number = serializers.CharField(
        max_length=20,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )

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
        allowed_roles = {
            CustomUser.Role.TENANT,
            CustomUser.Role.AGENT,
            CustomUser.Role.LANDLORD,
        }

        if value not in allowed_roles:
            raise serializers.ValidationError(
                "This account role cannot register through this endpoint."
            )

        return value

    def validate_phone_number(self, value):
        try:
            return normalize_phone_number(
                value,
                default_region="NG",
            )
        except ValueError:
            raise serializers.ValidationError("Enter a valid phone number.")

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )

        email = attrs.get("email")

        if isinstance(email, str) and not email.strip():
            email = None
            attrs["email"] = None

        role = attrs.get("role")

        if (
            role
            in {
                CustomUser.Role.AGENT,
                CustomUser.Role.LANDLORD,
            }
            and not email
        ):
            raise serializers.ValidationError(
                {"email": "Email is required for agent and landlord accounts."}
            )

        # Validate uniqueness after phone-number normalization.
        if CustomUser.objects.filter(phone_number=attrs["phone_number"]).exists():
            raise serializers.ValidationError(
                {"phone_number": "An account with this phone number already exists."}
            )

        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                {"email": "An account with this email already exists."}
            )

        return attrs


# ==========================================
# VERIFY EMAIL OTP SERIALIZER
# ==========================================
class VerifyEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)


# ==========================================
# VERIFY PHONE OTP SERIALIZER
# ==========================================
class VerifyPhoneOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=20,
        trim_whitespace=True,
    )
    otp = serializers.CharField(min_length=6, max_length=6)

    def validate_phone_number(self, value):
        try:
            return normalize_phone_number(
                value,
                default_region="NG",
            )
        except ValueError:
            raise serializers.ValidationError("Enter a valid phone number.")

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numbers.")

        return value


# ==========================================
# RESEND EMAIL OTP SERIALIZER
# ==========================================
class ResendEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


# ==========================================
# RESEND PHONE OTP SERIALIZER
# ==========================================
class ResendPhoneOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


# ==========================================
# LOGIN SERIALIZER
# ==========================================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# ==========================================
# LOGIN SERIALIZER - MOBILE
# ==========================================


class MobileLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=20,
        trim_whitespace=True,
    )
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_phone_number(self, value):
        try:
            return normalize_phone_number(
                value,
                default_region="NG",
            )
        except ValueError:
            raise serializers.ValidationError("Enter a valid phone number.")


# ==========================================
# LOGGED IN USER SERIALIZER
# ==========================================
# class AuthUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = [
#             "id",
#             "slug",
#             "first_name",
#             "last_name",
#             "email",
#             "phone_number",
#             "role",
#             "is_verified",
#         ]


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
