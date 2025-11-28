# settings.py - Production-ready for Railway
from pathlib import Path
import os
from django.contrib.messages import constants as messages
import dj_database_url

# ------------------------------
# Paths
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------
# Security
# ------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-local-secret-replace-me")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

# ------------------------------
# Hosts
# ------------------------------
_allowed = os.environ.get("ALLOWED_HOSTS", "")
if _allowed:
    ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
else:
    ALLOWED_HOSTS = []

# ------------------------------
# Installed apps
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

# ------------------------------
# Middleware
# ------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files
]

# ------------------------------
# URL & WSGI
# ------------------------------
ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

# ------------------------------
# Templates
# ------------------------------
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
# Database
# ------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{str(BASE_DIR / 'db.sqlite3')}", conn_max_age=600
    )
}

# ------------------------------
# Password validation
# ------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------
# Internationalization
# ------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------
# Static files
# ------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------
# Default primary key
# ------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------
# Messages
# ------------------------------
MESSAGES_TAGS = {messages.ERROR: "danger"}

# ------------------------------
# Security headers for production
# ------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ------------------------------
# Ensure Django redirects /path -> /path/
# ------------------------------
APPEND_SLASH = True
