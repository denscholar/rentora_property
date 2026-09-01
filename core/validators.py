from pathlib import Path

from django.conf import settings
from rest_framework.exceptions import ValidationError


def validate_property_verification_document(file):
    """
    Validate an uploaded property verification document.

    Supported formats:
        - PDF
        - JPG
        - JPEG
        - PNG
    """

    if not file:
        raise ValidationError(
            "A property verification document is required."
        )

    # ---------------------------------------------------------
    # File size
    # ---------------------------------------------------------
    max_size = getattr(
        settings,
        "PROPERTY_VERIFICATION_DOCUMENT_MAX_SIZE",
        2 * 1024 * 1024,
    )

    if file.size == 0:
        raise ValidationError(
            "The uploaded document is empty."
        )

    if file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)

        raise ValidationError(
            f"The document must not exceed {max_size_mb:.0f} MB."
        )

    # ---------------------------------------------------------
    # File extension
    # ---------------------------------------------------------
    extension = Path(file.name).suffix.lower()

    allowed_extensions = getattr(
        settings,
        "PROPERTY_VERIFICATION_DOCUMENT_EXTENSIONS",
        {
            ".pdf",
            ".jpg",
            ".jpeg",
            ".png",
        },
    )

    if extension not in allowed_extensions:
        allowed = ", ".join(
            ext.replace(".", "").upper()
            for ext in sorted(allowed_extensions)
        )

        raise ValidationError(
            f"Unsupported document format. "
            f"Allowed formats are: {allowed}."
        )

    return file