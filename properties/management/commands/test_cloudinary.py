# =====================================================
# TEST CLOUDINARY CONNECTION
# =====================================================

from cloudinary import api
from cloudinary.exceptions import Error
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Verify the SheltaMe Cloudinary configuration."

    def handle(self, *args, **options):
        self.stdout.write("Testing Cloudinary connection...")

        if not settings.CLOUDINARY_CLOUD_NAME:
            self.stderr.write(self.style.ERROR("CLOUDINARY_CLOUD_NAME is missing."))
            return

        if not settings.CLOUDINARY_API_KEY:
            self.stderr.write(self.style.ERROR("CLOUDINARY_API_KEY is missing."))
            return

        if not settings.CLOUDINARY_API_SECRET:
            self.stderr.write(self.style.ERROR("CLOUDINARY_API_SECRET is missing."))
            return

        try:
            result = api.ping()

        except Error as exc:
            self.stderr.write(self.style.ERROR(f"Cloudinary connection failed: {exc}"))
            return

        self.stdout.write(self.style.SUCCESS("Cloudinary connection successful."))

        self.stdout.write(f"Cloud name: {settings.CLOUDINARY_CLOUD_NAME}")

        self.stdout.write(f"Response: {result}")
