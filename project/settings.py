
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
env_hosts = os.environ.get("ALLOWED_HOSTS")
if env_hosts:
    ALLOWED_HOSTS = [h.strip() for h in env_hosts.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = [
        "127.0.0.1",
        "localhost",
        "makmedia-production.up.railway.app",
        "generous-vitality.up.railway.app",
        "www.makmedia.tech",
    ]

CSRF_TRUSTED_ORIGINS = [
    f"https://{h.strip()}" for h in ALLOWED_HOSTS if h and not h.startswith("127.") and not h.startswith("localhost")
]

# ------------------------------
# Security & SSL (Production)
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
# Database (robust handling)
# ------------------------------
DB_URL = os.environ.get("DATABASE_URL")

if DB_URL:
    # Parse URL and build DB config.
    # dj_database_url will return a dict usable by Django.
    # Force SSL in non-debug to satisfy managed Postgres providers.
    default_db = dj_database_url.parse(DB_URL, conn_max_age=600)
    if not DEBUG:
        # Ensure SSL (some providers require sslmode)
        default_db.setdefault("OPTIONS", {})
        # psycopg expects 'sslmode' string
        default_db["OPTIONS"].setdefault("sslmode", "require")
    DATABASES = {"default": default_db}
else:
    # Local development fallback (keeps current local SQLite behaviour)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
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
    "cloudinary_storage",
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


# Static files (CSS, JS, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------
# Media files
# ------------------------------
MEDIA_URL = "/media/"

USE_CLOUDINARY = not DEBUG

if USE_CLOUDINARY:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

    STORAGES = {
        "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }

else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = BASE_DIR / "media"

    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }


# ------------------------------
# Internationalization
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------
# Default primary key & messages
# ------------------------------
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
