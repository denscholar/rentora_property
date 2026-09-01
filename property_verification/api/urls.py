from django.urls import path

from property_verification.api.views.authorization import (
    PropertyVerificationAuthorizationAPIView,
)
from property_verification.api.views.initiation import (
    InitiatePropertyVerificationAPIView,
)
from property_verification.api.views.property_verification_document import (
    PublicPropertyVerificationDocumentDeleteAPIView,
    PublicPropertyVerificationDocumentListAPIView,
    PublicPropertyVerificationDocumentUploadAPIView,
)
from property_verification.api.views.property_verification_review import (
    SubmitPropertyVerificationForReviewAPIView,
)
from property_verification.api.views.verification import (
    PublicPropertyVerificationAPIView,
)

urlpatterns = [
    path(
        "submissions/<uuid:submission_uuid>/initiate/",
        InitiatePropertyVerificationAPIView.as_view(),
        name="initiate-property-verification",
    ),
    path(
        "public/<str:token>/",
        PublicPropertyVerificationAPIView.as_view(),
        name="public-property-verification",
    ),
    path(
        "authorize/<str:token>/",
        PropertyVerificationAuthorizationAPIView.as_view(),
        name="property-verification-authorize",
    ),
    path(
        "public/<uuid:verification_uuid>/<str:token>/documents/",
        PublicPropertyVerificationDocumentUploadAPIView.as_view(),
        name="public-property-verification-document-upload",
    ),
    path(
        "public/<uuid:verification_uuid>/<str:token>/documents/list/",
        PublicPropertyVerificationDocumentListAPIView.as_view(),
        name="public-property-verification-document-list",
    ),
    path(
        "public/<uuid:verification_uuid>/<str:token>/documents/<uuid:document_uuid>/",
        PublicPropertyVerificationDocumentDeleteAPIView.as_view(),
        name="public-property-verification-document-delete",
    ),
    path(
        "public<uuid:uuid>/submit-for-review/",
        SubmitPropertyVerificationForReviewAPIView.as_view(),
        name="submit-property-verification-for-review",
    ),
]
