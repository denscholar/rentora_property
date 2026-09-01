from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
    # Public frontend
    path(
        "",
        include("frontend.urls"),
    ),
    path(
        "api/accounts/",
        include("accounts.urls"),
    ),
    path(
        "api/properties/",
        include("properties.api.urls"),
    ),
    path(
        "api/locations/",
        include("locations.urls", namespace="locate"),
    ),
    path(
        "api/property-moderation/",
        include("locations.urls"),
    ),
    path(
        "api/property-verification/",
        include("property_verification.api.urls"),
    ),
    path(
        "api/property-verification-admin/",
        include("property_verification_admin.urls"),
    ),
]


# urlpatterns = [path("api/v1/", include(urlpatterns))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
