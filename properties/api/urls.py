from django.urls import path

from properties.api.views.media import (
    PropertySubmissionMediaDeleteAPIView,
    PropertySubmissionMediaListCreateAPIView,
    PropertySubmissionMediaSetCoverAPIView,
)

from .views import (
    ArchivePropertySubmissionAPIView,
    PropertySubmissionDetailAPIView,
    PropertySubmissionListCreateAPIView,
    SubmitPropertySubmissionAPIView,
)
from .views.lookups import (
    AmenityCategoryLookupAPIView,
    AmenityLookupAPIView,
    FurnishingStatusLookupAPIView,
    PaymentFrequencyListAPIView,
    PropertyConditionLookupAPIView,
    PropertyPurposeLookupAPIView,
    PropertyTypeLookupAPIView,
)

app_name = "properties"


urlpatterns = [
    path(
        "lookups/property-types/",
        PropertyTypeLookupAPIView.as_view(),
        name="property-type-lookups",
    ),
    path(
        "lookups/property-purposes/",
        PropertyPurposeLookupAPIView.as_view(),
        name="property-purpose-lookups",
    ),
    path(
        "lookups/property-conditions/",
        PropertyConditionLookupAPIView.as_view(),
        name="property-condition-lookups",
    ),
    path(
        "lookups/furnishing-statuses/",
        FurnishingStatusLookupAPIView.as_view(),
        name="furnishing-status-lookups",
    ),
    path(
        "lookups/amenity-categories/",
        AmenityCategoryLookupAPIView.as_view(),
        name="amenity-category-lookups",
    ),
    path(
        "lookups/amenities/",
        AmenityLookupAPIView.as_view(),
        name="amenity-lookups",
    ),
    path(
        "submissions/",
        PropertySubmissionListCreateAPIView.as_view(),
        name="submission-list-create",
    ),
    path(
        "submissions/<uuid:submission_uuid>/",
        PropertySubmissionDetailAPIView.as_view(),
        name="submission-detail",
    ),
    path(
        "submissions/<uuid:submission_uuid>/submit/",
        SubmitPropertySubmissionAPIView.as_view(),
        name="submission-submit",
    ),
    path(
        "submissions/<uuid:submission_uuid>/archive/",
        ArchivePropertySubmissionAPIView.as_view(),
        name="submission-archive",
    ),
    path(
        "lookups/payment-frequencies/",
        PaymentFrequencyListAPIView.as_view(),
        name="payment-frequency-list",
    ),
    path(
        "submissions/<uuid:submission_uuid>/media/",
        PropertySubmissionMediaListCreateAPIView.as_view(),
        name="submission-media-list-create",
    ),
    path(
        "submissions/<uuid:submission_uuid>/media/<uuid:media_uuid>/",
        PropertySubmissionMediaDeleteAPIView.as_view(),
        name="submission-media-delete",
    ),
    path(
        "submissions/<uuid:submission_uuid>/media/<uuid:media_uuid>/set-cover/",
        PropertySubmissionMediaSetCoverAPIView.as_view(),
        name="submission-media-set-cover",
    ),
]
