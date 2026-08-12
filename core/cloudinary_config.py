# =====================================================
# CLOUDINARY CONFIGURATION
# =====================================================

import cloudinary
from django.conf import settings


def configure_cloudinary() -> None:
    """
    Configure the official Cloudinary SDK using values loaded
    from Django settings.
    """

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=settings.CLOUDINARY_SECURE,
    )
