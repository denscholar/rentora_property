from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from property_verification.models.verification import PropertyVerification
from property_verification.api.serializers.verification import (
    PublicPropertyVerificationSerializer,
)
from property_verification.services.verification_service import (
    PropertyVerificationService,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse


class PublicPropertyVerificationAPIView(APIView):
    """
    Public endpoint used by a landlord/lawyer representative
    to review a property verification request.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Property Verification"],
        summary="Retrieve public property verification",
        description=(
            "Returns the details of a property verification request "
            "for a landlord or authorized representative using a "
            "verification token."
        ),
        responses={
            200: PublicPropertyVerificationSerializer,
            400: OpenApiResponse(
                description="Invalid verification token.",
            ),
            404: OpenApiResponse(
                description="Verification request not found.",
            ),
        },
    )
    def get(self, request, token):
        try:
            verification = PropertyVerificationService.get_public_verification(token)

            serializer = PublicPropertyVerificationSerializer(verification)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PropertyVerification.DoesNotExist:
            return Response(
                {"detail": ("Verification request not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )
