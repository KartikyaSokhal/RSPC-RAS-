from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler as drf_exception_handler


class ServiceError(APIException):
    def __init__(self, code, message, status=400):
        self.status_code = status
        super().__init__({"code": code, "message": message})


def exception_handler(exc, context):
    from django.db import OperationalError, ProgrammingError
    from rest_framework.response import Response
    if isinstance(exc, (OperationalError, ProgrammingError)):
        return Response({"error": {"code": "service_unavailable", "message": "The library is temporarily unavailable."}}, status=503, headers={"Cache-Control": "no-store"})
    response = drf_exception_handler(exc, context)
    if response is not None:
        if isinstance(exc, ServiceError):
            response.data = {"error": response.data}
        else:
            codes = {400: "invalid_request", 403: "forbidden", 404: "not_found", 405: "method_not_allowed", 429: "rate_limited"}
            response.data = {"error": {"code": codes.get(response.status_code, "request_failed"),
                                       "message": "This request could not be completed."}}
        response["Cache-Control"] = "no-store"
    return response
