import traceback
from django.utils.timezone import now
from django.http import HttpRequest

from .utils import log_activity

class GlobalExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            return self.get_response(request)
        except Exception as exc:
            self.handle_exception(request, exc)
            # Re-raise so Django can return proper 500 response
            raise

    def handle_exception(self, request: HttpRequest, exception: Exception):
        try:
            user = request.user if request.user.is_authenticated else None
        except Exception:
            user = None

        details = {
            "path": request.path,
            "method": request.method,
            "exception_type": exception.__class__.__name__,
            "exception_message": str(exception),
            "traceback": traceback.format_exc(limit=5),
        }

        log_activity(
            user=user,
            action="SYSTEM_ERROR",
            details=details,
            request=request,
            status="failed",
            log_file="errors",
        )