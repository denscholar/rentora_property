from django.conf import settings
from django.core.mail import send_mail


# ==========================================
# SEND EMAIL OTP
# ==========================================
def send_email_otp(user, otp):
    subject = "Verify your Rentora account"

    message = f"""
        Hello {user.first_name},
        Welcome to Rentora.
        Your verification OTP is:
        {otp}
        This OTP expires in 10 minutes.
        If you did not create this account, please ignore this email.
        Rentora Team
        """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
