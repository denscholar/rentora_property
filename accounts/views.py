from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from accounts.services.authentication import (
    authenticate_user,
    login_user,
    logout_user,
)


from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)


from accounts.selectors.user import get_user_by_email
from accounts.serializers import (
    AuthUserSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResendEmailOTPSerializer,
    VerifyEmailOTPSerializer,
)
from accounts.services.registration import register_user
from accounts.services.otp import (
    validate_email_otp,
    mark_email_verified,
    generate_email_otp,
)
from accounts.services.email import send_email_otp
from core.api.responses import error_response, success_response
from core.constants.response_codes import (
    ACCOUNT_ALREADY_VERIFIED,
    EMAIL_VERIFIED,
    INVALID_OTP,
    LOGIN_FAILED,
    LOGIN_SUCCESSFUL,
    LOGOUT_SUCCESSFUL,
    OTP_RESENT,
    REGISTRATION_SUCCESS_OTP_SENT,
    USER_NOT_FOUND,
    VALIDATION_ERROR,
)


# ==========================================
# REGISTER USER API
# ==========================================
@extend_schema(
    tags=["Authentication"],
    summary="Register User",
    description="""
Register a new Rentora user.

After registration, an OTP is sent to the user's email.
The account remains unverified until the OTP is confirmed.

Allowed roles:
- tenant
- agent
- landlord

Admin users cannot register through this endpoint.
""",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            description="Registration successful.",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "success": True,
                        "code": "REGISTRATION_SUCCESS_OTP_SENT",
                        "message": "Registration successful. OTP has been sent to your email for verification.",
                        "data": {
                            "email": "tenant@example.com",
                            "role": "tenant",
                            "is_verified": False,
                        },
                    },
                )
            ],
        ),
        400: OpenApiResponse(description="Validation error."),
    },
)
class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Registration failed",
                code=VALIDATION_ERROR,
                errors=serializer.errors,
            )

        user = register_user(serializer.validated_data)

        return success_response(
            message="Registration successful. OTP has been sent to your email.",
            code=REGISTRATION_SUCCESS_OTP_SENT,
            data={
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
            },
            status_code=status.HTTP_201_CREATED,
        )


# ==========================================
# VERIFY EMAIL OTP API
# ==========================================
@extend_schema(
    tags=["Authentication"],
    summary="Verify Email OTP",
    description="""
        Verify the OTP sent to the user's registered email address.

        When successful:
        - Account becomes verified.
        - OTP is cleared.
        - Verification timestamp is saved.
        """,
    request=VerifyEmailOTPSerializer,
    responses={
        200: OpenApiResponse(
            description="Email verified.",
            examples=[
                OpenApiExample(
                    "Success",
                    value={
                        "success": True,
                        "code": "EMAIL_VERIFIED",
                        "message": "Email verified successfully.",
                    },
                )
            ],
        ),
        400: OpenApiResponse(description="Invalid or expired OTP."),
        404: OpenApiResponse(description="User not found."),
    },
)
class VerifyEmailOTPAPIView(APIView):

    def post(self, request):
        serializer = VerifyEmailOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Invalid request data",
                code=VALIDATION_ERROR,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = get_user_by_email(email)

        if not user:
            return error_response(
                message="No account found with this email.",
                code=USER_NOT_FOUND,
                errors=serializer.errors,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return success_response(
                message="Account is already verified.",
                code=ACCOUNT_ALREADY_VERIFIED,
                status_code=status.HTTP_200_OK,
            )

        if not validate_email_otp(user, otp):
            return error_response(
                message="Invalid or expired OTP.",
                code=INVALID_OTP,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        mark_email_verified(user)

        return success_response(
            message="Email verified successfully.",
            code=EMAIL_VERIFIED,
            status_code=status.HTTP_200_OK,
        )


# ==========================================
# RESEND EMAIL OTP API
# ==========================================
@extend_schema(
    tags=["Authentication"],
    summary="Resend Email OTP",
    description="""
Generate and send a new OTP to the registered email.

Only unverified users can request a new OTP.
""",
    request=ResendEmailOTPSerializer,
    responses={
        200: OpenApiResponse(description="OTP resent."),
        400: OpenApiResponse(description="Account already verified."),
        404: OpenApiResponse(description="User not found."),
    },
)
class ResendEmailOTPAPIView(APIView):

    def post(self, request):
        serializer = ResendEmailOTPSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Invalid request data.",
                code=VALIDATION_ERROR,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]

        user = get_user_by_email(email)

        if not user:
            return error_response(
                message="No account found with this email.",
                code=USER_NOT_FOUND,
                errors=serializer.errors,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return error_response(
                message="Account already verified",
                code=ACCOUNT_ALREADY_VERIFIED,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        otp = generate_email_otp(user)
        send_email_otp(user, otp)

        return success_response(
            message="A new OTP has been sent to your email.",
            code=OTP_RESENT,
            data={},
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# LOGIN USER
# =====================================================
@extend_schema(
    tags=["Authentication"],
    summary="Login User",
    description="""
Login a verified Rentora user using email and password.

This endpoint uses Django Session Authentication.
A user must verify their email OTP before login.
""",
    request=LoginSerializer,
)
class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Invalid login credentials.",
                code=VALIDATION_ERROR,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = authenticate_user(
                request=request,
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            login_user(request, user)

        except ValidationError as exc:
            return error_response(
                message=str(exc),
                code=LOGIN_FAILED,
                errors=None,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Login successful.",
            code=LOGIN_SUCCESSFUL,
            data=AuthUserSerializer(user).data,
            status_code=status.HTTP_200_OK,
        )


# =====================================================
# LOGOUT USER
# =====================================================
@extend_schema(
    tags=["Authentication"],
    summary="Logout User",
    description="Logout the currently authenticated session user.",
)
class LogoutAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout_user(request)

        return success_response(
            message="Logout successfully",
            code=LOGOUT_SUCCESSFUL,
            status_code=status.HTTP_200_OK,
        )
