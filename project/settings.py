from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
import os
from django.contrib.messages import constants as messages
import dj_database_url

# ------------------------------
# Base path
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Env / debug
# ------------------------------
# Use a single canonical DEBUG boolean (readable from env)
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

SECRET_KEY = os.environ.get("")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "unsafe-local-secret-replace-me"   # only for local dev
    else:
        raise ImproperlyConfigured("SECRET_KEY environment variable is required in production")

# ------------------------------
# Hosts & trusted origins
# ------------------------------
# Provide a comma-separated ALLOWED_HOSTS via env, with sensible defaults
_allowed = os.environ.get(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,makmedia-production.up.railway.app,generous-vitality.up.railway.app"
)
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]

# For HTTPS proxies, add these to CSRF trusted origins (include scheme!)
# If you deploy on other domains, add them to the env ALLOWED_HOSTS and here.
CSRF_TRUSTED_ORIGINS = [
    f"https://{h.strip()}" for h in ALLOWED_HOSTS if h and not h.startswith("127.") and not h.startswith("localhost")
]

# ------------------------------
# Proxy / SSL settings (for Railway, behind a proxy)
# ------------------------------
# Accept X-Forwarded-Proto header from the proxy to detect HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Redirect to HTTPS in production only
SECURE_SSL_REDIRECT = not DEBUG

# Optional extra hardening in production
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ------------------------------
# Database (Railway)
# ------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,  # require SSL in production
    )
}

# ------------------------------
# Rest of your settings (apps/middleware/templates/etc.)
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
]

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

# static, time zone, messages, default field, logging — keep as you had them
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MESSAGES_TAGS = {messages.ERROR: "danger"}
APPEND_SLASH = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# Media files (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
