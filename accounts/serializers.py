from rest_framework import serializers

from accounts.models import CustomUser


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