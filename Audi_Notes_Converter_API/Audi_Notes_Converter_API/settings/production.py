from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    "LebohangRadebe.pythonanywhere.com",
]

# SECURITY
# Required when running behind a proxy (PythonAnywhere)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Force HTTPS
SECURE_SSL_REDIRECT = True

# Cookies only sent over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent JavaScript access to session cookies
SESSION_COOKIE_HTTPONLY = True

# Prevent XSS & MIME sniffing
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# HTTP Strict Transport Security (enable AFTER HTTPS confirmed)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# EMAIL (Gmail SMTP – production ready)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# LOGGING
# Optional: silence console logging in prod
LOGGING["handlers"].pop("console", None)


# DJANGO REST FRAMEWORK (production defaults)
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
    "rest_framework.renderers.JSONRenderer",
)

# PASSWORDS & TOKENS
# Shorter reset window in production
PASSWORD_RESET_TIMEOUT = 60 * 15
