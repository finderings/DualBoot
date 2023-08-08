import os

from pathlib import Path

from .utils import strtobool

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-ti4k^9f$8y^#3_w0zca1w_jtnh-h1a@aw7r5l%(5w+to03_@24"

DEBUG = True

ALLOWED_HOSTS = ("*",)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "rest_framework_simplejwt",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "main.permissions.IsStaffDelete",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

ROLLBAR = {
    "access_token": "f428cee461d9460db2f620862d732aec",
    "environment": "development" if DEBUG else "production",
    "code_version": "1.0",
    "root": BASE_DIR,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
    "task_manager.log_utils.LoggingMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "task_manager": {
            "()": "task_manager.log_utils.RequestFormatter",
            "format": (
                "{asctime} {levelname} method={request.method} path={request.path_info}"
                "view={view.__qualname__} user={user_id} {message} remote={remote_addr} {message}"
                " processing_time={processing_time:.4f} seconds"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "task_manager",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.server": {"level": "INFO", "handlers": ["console"]},
    }
}

ROOT_URLCONF = "task_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "task_manager.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASSWORD"],
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "main.User"


EMAIL_USE_SSL = strtobool(os.environ.get("EMAIL_USE_SSL", "0"))
EMAIL_USE_TLS = strtobool(os.environ.get("EMAIL_USE_TLS", "0"))
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = os.environ["EMAIL_PORT"]

DJANGO_ENV = os.environ["DJANGO_ENV"]
if DJANGO_ENV != "dev":
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    PUBLIC_FILE_STORAGE = "core.storage_backends.S3PublicStorage"
    AWS_QUERYSTRING_EXPIRE = 10 * 60
    AWS_QUERYSTRING_AUTH = True
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_REGION_NAME = os.environ["AWS_REGION_NAME"]
    AWS_DEFAULT_ACL = "private"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
    MEDIA_URL = "/media/"

UPLOAD_MAX_SIZES: dict[str, int] = {
    "avatar_picture": 1 * 1024 * 1024,
}

CELERY_BROKER_URL = f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}/0"
CELERY_INCLUDE = ["task_manager.tasks"]
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_TRACK_STARTED = True
CELERY_SEND_TASK_SENT_EVENT = True
