import hashlib

from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from property_verification.api.serializers.authorization import (
    PropertyVerificationAuthorizationSerializer,
)
from property_verification.models import (
    PropertyVerification,
)


from property_verification.services.authorization_service import (
    PropertyVerificationAuthorizationService,
)


class PropertyVerificationAuthorizationAPIView(APIView):
    """
    Public endpoint used by a landlord or authorized
    representative to authorize an agent to market a property.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Property Verification"],
        summary="Authorize or reject property verification",
        description=(
            "Allows a landlord or authorized representative to "
            "approve or reject a property verification request "
            "using a public verification token."
        ),
        request=PropertyVerificationAuthorizationSerializer,
        responses={
            200: OpenApiResponse(
                description="Property authorization completed successfully.",
            ),
            400: OpenApiResponse(
                description="Invalid authorization request.",
            ),
            404: OpenApiResponse(
                description="Invalid or expired verification link.",
            ),
            410: OpenApiResponse(
                description="Verification link has expired.",
            ),
        },
    )
    def post(self, request, token):

        # =====================================================
        # 1. HASH RAW TOKEN
        # =====================================================

        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()

        # =====================================================
        # 2. FIND VERIFICATION
        # =====================================================

        try:
            verification = PropertyVerification.objects.select_related(
                "representative"
            ).get(token_hash=token_hash)

        except PropertyVerification.DoesNotExist:
            return Response(
                {"detail": ("Invalid or expired verification link.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # =====================================================
        # 3. CHECK TOKEN EXPIRY
        # =====================================================

        if verification.token_expires_at <= timezone.now():

            if verification.status not in {
                PropertyVerification.VerificationStatus.AUTHORIZED,
                PropertyVerification.VerificationStatus.VERIFIED,
            }:
                verification.status = PropertyVerification.VerificationStatus.EXPIRED

                verification.save(
                    update_fields=[
                        "status",
                        "updated_at",
                    ]
                )

            return Response(
                {"detail": ("This verification link has expired.")},
                status=status.HTTP_410_GONE,
            )

        # =====================================================
        # 4. VALIDATE REQUEST DATA
        # =====================================================

        serializer = PropertyVerificationAuthorizationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # =====================================================
        # 5. GET CLIENT INFORMATION
        # =====================================================

        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded_for:
            ip_address = forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        user_agent = request.META.get(
            "HTTP_USER_AGENT",
            "",
        )

        # =====================================================
        # 6. AUTHORIZE
        # =====================================================

        try:
            authorization = PropertyVerificationAuthorizationService.respond(
                verification,
                decision=serializer.validated_data["decision"],
                availability_confirmed=serializer.validated_data.get(
                    "availability_confirmed",
                    False,
                ),
                agent_authorized=serializer.validated_data.get(
                    "agent_authorized",
                    False,
                ),
                authorization_note=serializer.validated_data.get(
                    "authorization_note",
                    "",
                ),
                rejection_reason=serializer.validated_data.get(
                    "rejection_reason",
                    "",
                ),
                ip_address=ip_address,
                user_agent=user_agent,
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # 7. RESPONSE
        # =====================================================

        return Response(
            {
                "message": "Property authorization completed " "successfully.",
                "verification_status": (verification.get_status_display()),
                "authorized_at": (authorization.responded_at),
            },
            status=status.HTTP_200_OK,
        )
