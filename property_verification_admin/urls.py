from django.urls import path

from .api.views.list import PropertyVerificationAdminListAPIView
from .api.views.detail import PropertyVerificationAdminDetailAPIView
from .api.views.review import (
    PropertyVerificationAdminRejectAPIView,
    PropertyVerificationAdminVerifyAPIView,
)
from property_verification_admin.api.views.submission_detail import (
    PropertySubmissionAdminDetailAPIView,
)
from property_verification_admin.api.views.submission_review import (
    PropertySubmissionAdminApproveAPIView,
    PropertySubmissionAdminRejectAPIView,
)

urlpatterns = [
    path(
        "verifications/",
        PropertyVerificationAdminListAPIView.as_view(),
        name="admin-verification-list",
    ),
    path(
        "verifications/<uuid:uuid>/",
        PropertyVerificationAdminDetailAPIView.as_view(),
        name="admin-verification-detail",
    ),
    path(
        "verifications/<uuid:uuid>/approve/",
        PropertyVerificationAdminVerifyAPIView.as_view(),
        name="admin-verification-approve",
    ),
    path(
        "verifications/<uuid:uuid>/reject/",
        PropertyVerificationAdminRejectAPIView.as_view(),
        name="admin-verification-reject",
    ),
    path(
        "submissions/<uuid:submission_uuid>/",
        PropertySubmissionAdminDetailAPIView.as_view(),
        name="admin-submission-detail",
    ),
    path(
        "submissions/<uuid:submission_uuid>/approve/",
        PropertySubmissionAdminApproveAPIView.as_view(),
        name="admin-submission-approve",
    ),
    path(
        "submissions/<uuid:submission_uuid>/reject/",
        PropertySubmissionAdminRejectAPIView.as_view(),
        name="admin-submission-reject",
    ),
]
