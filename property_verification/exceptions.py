# ============================================================
# EXCEPTIONS
# ============================================================


class PropertyVerificationDocumentError(Exception):
    """
    Base exception for property verification document
    operations.
    """


class PropertyVerificationDocumentUploadError(PropertyVerificationDocumentError):
    """
    Raised when Cloudinary cannot upload the document.
    """


class PropertyVerificationDocumentSaveError(PropertyVerificationDocumentError):
    """
    Raised when the uploaded document metadata cannot be saved.
    """


class PropertyVerificationDocumentAuthorizationError(PropertyVerificationDocumentError):
    """
    Raised when the verification is not allowed to receive
    documents.
    """
