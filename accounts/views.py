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


from accounts.selectors.user_selectors import get_user_by_email
from accounts.serializers import AuthUserSerializer, LoginSerializer, RegisterSerializer, ResendEmailOTPSerializer, VerifyEmailOTPSerializer
from accounts.services.registration import register_user
from accounts.services.otp import (
    validate_email_otp,
    mark_email_verified,
    generate_email_otp,
)
from accounts.services.email import send_email_otp


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
            return Response(
                {
                    "success": False,
                    "code": "VALIDATION_ERROR",
                    "message": "Registration failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = register_user(serializer.validated_data)

        return Response(
            {
                "success": True,
                "code": "REGISTRATION_SUCCESS_OTP_SENT",
                "message": "Registration successful. OTP has been sent to your email for verification.",
                "data": {
                    "email": user.email,
                    "role": user.role,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_201_CREATED,
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
            return Response(
                {
                    "success": False,
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = get_user_by_email(email)

        if not user:
            return Response(
                {
                    "success": False,
                    "code": "USER_NOT_FOUND",
                    "message": "No account found with this email.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {
                    "success": True,
                    "code": "ACCOUNT_ALREADY_VERIFIED",
                    "message": "Account is already verified.",
                },
                status=status.HTTP_200_OK,
            )

        if not validate_email_otp(user, otp):
            return Response(
                {
                    "success": False,
                    "code": "INVALID_OR_EXPIRED_OTP",
                    "message": "Invalid or expired OTP.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        mark_email_verified(user)

        return Response(
            {
                "success": True,
                "code": "EMAIL_VERIFIED",
                "message": "Email verified successfully.",
            },
            status=status.HTTP_200_OK,
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
            return Response(
                {
                    "success": False,
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request data.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]

        user = get_user_by_email(email)

        if not user:
            return Response(
                {
                    "success": False,
                    "code": "USER_NOT_FOUND",
                    "message": "No account found with this email.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {
                    "success": False,
                    "code": "ACCOUNT_ALREADY_VERIFIED",
                    "message": "Account is already verified.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = generate_email_otp(user)
        send_email_otp(user, otp)

        return Response(
            {
                "success": True,
                "code": "OTP_RESENT",
                "message": "A new OTP has been sent to your email.",
            },
            status=status.HTTP_200_OK,
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
            return Response(
                {
                    "success": False,
                    "code": "VALIDATION_ERROR",
                    "message": "Login failed.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = authenticate_user(
                request=request,
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )

            login_user(request, user)

        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "code": "LOGIN_FAILED",
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "code": "LOGIN_SUCCESSFUL",
                "message": "Login successful.",
                "data": AuthUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
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

        return Response(
            {
                "success": True,
                "code": "LOGOUT_SUCCESSFUL",
                "message": "Logout successful.",
            },
            status=status.HTTP_200_OK,
        )