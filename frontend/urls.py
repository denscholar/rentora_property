from django.urls import path

from frontend.views import (
    DashboardPageView,
    LandingPageView,
    LoginPageView,
    PropertySubmissionCreatePageView,
    PropertySubmissionDetailWizardPageView,
    PropertySubmissionListPageView,
    PropertySubmissionWizardPageView,
    RegisterPageView,
    VerifyEmailPageView,
)

app_name = "frontend"


urlpatterns = [
    path(
        "",
        LandingPageView.as_view(),
        name="landing-page",
    ),
    path(
        "register/",
        RegisterPageView.as_view(),
        name="register",
    ),
    path(
        "verify-email/",
        VerifyEmailPageView.as_view(),
        name="verify-email",
    ),
    path(
        "login/",
        LoginPageView.as_view(),
        name="login",
    ),
    path(
        "dashboard/",
        DashboardPageView.as_view(),
        name="dashboard",
    ),
    path(
        "dashboard/submissions/",
        PropertySubmissionListPageView.as_view(),
        name="property-submission-list",
    ),
    path(
        "dashboard/submissions/create/",
        PropertySubmissionCreatePageView.as_view(),
        name="property-submission-create",
    ),
    path(
        "dashboard/submissions/<uuid:submission_uuid>/edit/",
        PropertySubmissionWizardPageView.as_view(),
        name="property-submission-edit",
    ),
    path(
        "dashboard/submissions/<uuid:submission_uuid>/detail/",
        PropertySubmissionDetailWizardPageView.as_view(),
        name="property-submission-detail",
    ),
]
