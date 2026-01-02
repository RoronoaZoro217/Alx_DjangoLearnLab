from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Email → console only
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"