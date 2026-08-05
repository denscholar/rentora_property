from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



class LandingPageView(TemplateView):
    template_name = "frontend/landing.html"


class LandingPageView(TemplateView):
    template_name = "frontend/landing.html"


class RegisterPageView(TemplateView):
    template_name = "frontend/auth/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("frontend:dashboard")

        return super().dispatch(request, *args, **kwargs)


class VerifyEmailPageView(TemplateView):
    template_name = "frontend/auth/verify_email.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("frontend:dashboard")

        return super().dispatch(request, *args, **kwargs)


class LoginPageView(TemplateView):
    template_name = "frontend/auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("frontend:dashboard")

        return super().dispatch(request, *args, **kwargs)


class DashboardPageView(TemplateView):
    template_name = "frontend/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("frontend:login")

        return super().dispatch(request, *args, **kwargs)


class DashboardPageView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "frontend/dashboard.html"
    login_url = "frontend:login"


# class PropertySubmissionListPageView(
#     LoginRequiredMixin,
#     TemplateView,
# ):
#     template_name = "frontend/dashboard/submissions/list.html"
#     login_url = "frontend:login"


class PropertySubmissionListPageView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "frontend/dashboard/submissions/list.html"

    login_url = "frontend:login"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in {
            "agent",
            "landlord",
        }:
            return redirect("frontend:dashboard")

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )



class PropertySubmissionCreatePageView(
    LoginRequiredMixin,
    TemplateView,
):
    """
    Renders the property-submission wizard shell.

    Lookup data and submission actions are handled through the
    REST API using JavaScript.
    """

    template_name = (
        "frontend/dashboard/submissions/create.html"
    )

    login_url = "frontend:login"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in {
            "agent",
            "landlord",
        }:
            return redirect("frontend:dashboard")

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )