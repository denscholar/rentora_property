from rest_framework.response import Response
from rest_framework import status


# =====================================================
# SUCCESS RESPONSE
# =====================================================

def success_response(
    *,
    message,
    data=None,
    code="SUCCESS",
    status_code=status.HTTP_200_OK,
):
    """
    Standard success response.
    """

    return Response(
        {
            "success": True,
            "code": code,
            "message": message,
            "data": data,
        },
        status=status_code,
    )



# =====================================================
# ERROR RESPONSE
# =====================================================

def error_response(
    *,
    message,
    code="ERROR",
    errors=None,
    status_code=status.HTTP_400_BAD_REQUEST,
):
    """
    Standard error response.
    """

    return Response(
        {
            "success": False,
            "code": code,
            "message": message,
            "errors": errors,
        },
        status=status_code,
    )