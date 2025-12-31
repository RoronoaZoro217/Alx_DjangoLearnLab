import json
import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import ActivityLog

User = get_user_model()

# Logger registry (matches settings.LOGGING)
LOGGERS = {
    "auth": logging.getLogger("auth"),
    "documents": logging.getLogger("documents"),
    "audio": logging.getLogger("audio"),
    "errors": logging.getLogger("errors"),
}

# Helper: Get client IP address safely
def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
    except Exception:
        return None

# Core logging utility
def log_activity(
    *,
    request=None,
    user=None,
    action,
    details=None,
    category="errors",
    status="success",
):
    try:
        # Resolve user
        if user is None and request and request.user.is_authenticated:
            user = request.user

        if user and not isinstance(user, User):
            user = None
        # Resolve IP
        ip_address = get_client_ip(request) if request else None

        # Normalize details
        if isinstance(details, (dict, list)):
            details_str = json.dumps(details, ensure_ascii=False)
        else:
            details_str = str(details) if details else ""
        # Save to database
        ActivityLog.objects.create(
            user=user,
            action=action,
            details=details_str,
            ip_address=ip_address,
            status=status,
            timestamp=timezone.now(),
        )

        # Write to file logger
        logger = LOGGERS.get(category, LOGGERS["errors"])

        logger.info(
            "[%s] user=%s ip=%s action=%s details=%s",
            status.upper(),
            user.id if user else "anonymous",
            ip_address,
            action,
            details_str,
        )
    except Exception as e:
        logging.getLogger("errors").error(
            "Logging failure: %s", str(e), exc_info=True
        )
