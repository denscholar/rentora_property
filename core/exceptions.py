from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from properties.exceptions.base import DomainException


def custom_exception_handler(exc, context):
    """
    Convert domain exceptions into API responses.
    """

    if isinstance(exc, DomainException):

        if hasattr(exc, "errors"):
            return Response(
                exc.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "detail": exc.message,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return exception_handler(exc, context)
