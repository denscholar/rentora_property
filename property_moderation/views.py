from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from properties.api.permissions import IsPropertyModerator
from properties.models import PropertySubmission
from .serializers import (
    PropertyModerationSubmissionDetailSerializer,
    PropertyModerationSubmissionListSerializer,
)


class PropertyModerationSubmissionListAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPropertyModerator,
    ]

    permission_code = "property_moderation.view"

    def get(self, request):
        submissions = (
            PropertySubmission.objects.filter(
                status=PropertySubmission.Status.UNDER_REVIEW
            )
            .select_related(
                "submitted_by",
                "property_type",
                "purpose",
                "area",
            )
            .order_by("-created_at")
        )

        serializer = PropertyModerationSubmissionListSerializer(
            submissions,
            many=True,
        )

        return Response(
            {
                "success": True,
                "message": "Property moderation submissions retrieved successfully.",
                "count": submissions.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class PropertyModerationSubmissionDetailAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsPropertyModerator,
    ]

    permission_code = "property_moderation.view"

    def get(self, request, uuid):
        submission = (
            PropertySubmission.objects.select_related(
                "submitted_by",
                "property_group",
                "property_type",
                "purpose",
                "property_condition",
                "furnishing_status",
                "area",
                "reviewed_by",
            )
            .prefetch_related(
                "amenities",
            )
            .filter(
                id=uuid,
            )
            .first()
        )

        if not submission:
            return Response(
                {
                    "success": False,
                    "message": "Property submission not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PropertyModerationSubmissionDetailSerializer(submission)

        return Response(
            {
                "success": True,
                "message": ("Property submission details " "retrieved successfully."),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
