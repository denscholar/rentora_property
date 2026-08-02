from django.urls import path

from .views import (
    ArchivePropertySubmissionAPIView,
    PropertySubmissionDetailAPIView,
    PropertySubmissionListCreateAPIView,
    SubmitPropertySubmissionAPIView,
)
from .views.lookups import AmenityCategoryLookupAPIView, AmenityLookupAPIView, FurnishingStatusLookupAPIView, PropertyConditionLookupAPIView, PropertyPurposeLookupAPIView, PropertyTypeLookupAPIView

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
        "properties/submissions/",
        PropertySubmissionListCreateAPIView.as_view(),
        name="submission-list-create",
    ),
    path(
        "properties/submissions/<uuid:submission_uuid>/",
        PropertySubmissionDetailAPIView.as_view(),
        name="submission-detail",
    ),
    path(
        "properties/submissions/<uuid:submission_uuid>/submit/",
        SubmitPropertySubmissionAPIView.as_view(),
        name="submission-submit",
    ),
    path(
        "properties/submissions/<uuid:submission_uuid>/archive/",
        ArchivePropertySubmissionAPIView.as_view(),
        name="submission-archive",
    ),
]
