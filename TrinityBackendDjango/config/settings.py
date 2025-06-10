import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

#
# django-tenants configuration
#
SHARED_APPS = [
    "django_tenants",

    # tenant model
    "apps.tenants",

    # Django contrib (shared)
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party shared
    "corsheaders",
    "rest_framework",
    "guardian",
    "simple_history",
]

TENANT_APPS = [
    "apps.accounts",
    "apps.registry",
    "apps.subscriptions",
    "apps.workflows",
    "apps.atoms",
    "apps.atom_configs",
    "apps.config_store",
    "apps.permissions",
    "apps.orchestration",
    "apps.roles",
    "apps.audit",
]

INSTALLED_APPS = SHARED_APPS + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

# Specify tenant & domain models by app_label.ModelName
TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"

#
# Database routers (required by django-tenants)
#
DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

#
# Middleware
#
MIDDLEWARE = [
    "django_tenants.middleware.TenantMiddleware",  # must be first
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL conf
ROOT_URLCONF = "config.urls"
PUBLIC_SCHEMA_URLCONF = "config.urls"

#
# Templates
#
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
    },
]

# WSGI & ASGI
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

#
# Databases
#
DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.getenv("POSTGRES_DB", "trinity_db"),
        "USER": os.getenv("POSTGRES_USER", "trinity_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "trinity_pass"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/trinity")

# Redis for cache & Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

#
# Authentication & Permissions
#
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)
ANONYMOUS_USER_NAME = None

#
# Django REST Framework
#
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

#
# Static & media files
#
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

#
# CORS
#
CORS_ALLOW_ALL_ORIGINS = True


#
# Celery
#
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

#
# django-simple-history
#
SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
