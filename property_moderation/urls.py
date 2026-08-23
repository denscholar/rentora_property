from django.urls import path

from .views import (
    PropertyModerationSubmissionDetailAPIView,
    PropertyModerationSubmissionListAPIView,
)

urlpatterns = [
    path(
        "submissions/",
        PropertyModerationSubmissionListAPIView.as_view(),
        name="property-moderation-submissions",
    ),
    path(
        "submissions/<uuid:uuid>/",
        PropertyModerationSubmissionDetailAPIView.as_view(),
        name="property-moderation-submission-detail",
    ),
]
