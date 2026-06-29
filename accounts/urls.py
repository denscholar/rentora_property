from django.urls import path

from accounts.views import (
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    ResendEmailOTPAPIView,
    VerifyEmailOTPAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-email-otp/", VerifyEmailOTPAPIView.as_view(), name="verify-email-otp"),
    path("resend-email-otp/", ResendEmailOTPAPIView.as_view(), name="resend-email-otp"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
