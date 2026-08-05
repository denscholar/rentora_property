from django.urls import path

from locations.views import (
    AreaListAPIView,
    CountryListAPIView,
    LGAListAPIView,
    StateListAPIView,
)

app_name = "locations"


urlpatterns = [
    path(
        "countries/",
        CountryListAPIView.as_view(),
        name="country-list",
    ),
    path(
        "states/",
        StateListAPIView.as_view(),
        name="state-list",
    ),
    path(
        "lgas/",
        LGAListAPIView.as_view(),
        name="lga-list",
    ),
    path(
        "areas/",
        AreaListAPIView.as_view(),
        name="area-list",
    ),
]
