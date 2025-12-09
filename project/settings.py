# settings.py

from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages
import dj_database_url

# ------------------------------
# Base directory
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Debug & Secret Key
# ------------------------------
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "unsafe-local-secret-replace-me"
    else:
        raise ImproperlyConfigured("SECRET_KEY environment variable is required in production")

# ------------------------------
# Allowed Hosts & CSRF
# ------------------------------
_allowed = os.environ.get(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,makmedia-production.up.railway.app,generous-vitality.up.railway.app"
)
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [
    f"https://{h.strip()}" for h in ALLOWED_HOSTS if h and not h.startswith("127.") and not h.startswith("localhost")
]

# ------------------------------
# Security & SSL (Railway)
# ------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = not DEBUG
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ------------------------------
# Database
# ------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# ------------------------------
# Installed Apps
# ------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",
    "main",
    "cloudinary",
    "cloudinary_storage",  # Django Cloudinary storage backend
]

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ------------------------------
# Templates
# ------------------------------
ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# ------------------------------
# Static files (WhiteNoise)
# ------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------
# Media files (Cloudinary)
# ------------------------------
# All FileField/ImageField uploads will be stored in Cloudinary
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Optional: keep MEDIA_URL for legacy templates (Cloudinary provides its own URLs)
MEDIA_URL = "/media/"

# ------------------------------
# Internationalization
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MESSAGES_TAGS = {messages.ERROR: "danger"}
APPEND_SLASH = True

# ------------------------------
# Logging
# ------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
