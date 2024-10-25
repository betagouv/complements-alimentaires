"""
Django settings for complalim project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent

# Environment
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET")
SECURE_SSL_REDIRECT = env("FORCE_HTTPS", cast=bool)

SECURE = env("SECURE", cast=bool)
PROTOCOL = "https" if SECURE else "http"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool)
AUTH_USER_MODEL = "data.User"

ALLOWED_HOSTS = [x.strip() for x in env("ALLOWED_HOSTS", cast=list)]

ENVIRONMENT = env("ENVIRONMENT")

ENABLE_SILK = env("ENABLE_SILK", cast=bool, default=False)

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "webpack_loader",
    "django_ckeditor_5",
    "anymail",
    "simple_history",
    "django_extensions",
    "phonenumber_field",
    "hijack",
    "hijack.contrib.admin",
]

if ENABLE_SILK:
    THIRD_PARTY_APPS.append("silk")

PROJECT_APPS = [
    "config",
    "api",
    "data",
    "tokens",
    "web",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "hijack.middleware.HijackUserMiddleware",
]

if ENABLE_SILK:
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")

CSRF_COOKIE_NAME = "csrftoken"
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "data/admin/templates")],
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

WSGI_APPLICATION = "config.wsgi.application"

# Webpack
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "frontend/dist/")]
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "/bundles/",
        "STATS_FILE": os.path.join(FRONTEND_DIR, "webpack-stats.json"),
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": env("DB_USER"),
        "NAME": env("DB_NAME"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "CONN_MAX_AGE": 60,
    }
}

REDIS_URL = os.getenv("REDIS_URL")
REDIS_PREPEND_KEY = os.getenv("REDIS_PREPEND_KEY", "")

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "fr-fr"
LANGUAGES = (("fr", "Français"),)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "templates", "locale"),
]

TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media and file storage

default_file_storage = env("DEFAULT_FILE_STORAGE")

STORAGES = {
    "default": {
        "BACKEND": default_file_storage,
    },
    "staticfiles": {
        "BACKEND": env("STATICFILES_STORAGE"),
    },
}

if default_file_storage == "storages.backends.s3.S3Storage":
    AWS_ACCESS_KEY_ID = env("CELLAR_KEY")
    AWS_SECRET_ACCESS_KEY = env("CELLAR_SECRET")
    AWS_S3_ENDPOINT_URL = env("CELLAR_HOST")
    AWS_STORAGE_BUCKET_NAME = env("CELLAR_BUCKET_NAME")
    AWS_LOCATION = "media"
    AWS_QUERYSTRING_AUTH = False

MEDIA_ROOT = env("MEDIA_ROOT", default=os.path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

SESSION_COOKIE_AGE = 31536000
SESSION_COOKIE_SECURE = env("SECURE", cast=bool)
SESSION_COOKIE_HTTPONLY = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/s-identifier"

HOSTNAME = env("HOSTNAME")

# Email
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = env("CONTACT_EMAIL")
EMAIL_BACKEND = env("EMAIL_BACKEND")

if DEBUG and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025

NEWSLETTER_BREVO_LIST_ID = env("NEWSLETTER_BREVO_LIST_ID", cast=int, default=None)
ANYMAIL = {
    "SENDINBLUE_API_KEY": env("BREVO_API_KEY", default=None),
}

# Rest framework

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "UPLOADED_FILES_USE_URL": True,
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "api.exception_handling.custom_exception_handler",
}

# logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# CK Editor 5

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

if default_file_storage == "storages.backends.s3.S3Storage":
    CKEDITOR_5_FILE_STORAGE = "data.storage.FileUploadS3Storage"
else:
    CKEDITOR_5_FILE_STORAGE = "data.storage.FileUploadFileSystemStorage"


CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "fr",
        "toolbar": [
            "heading",
            "blockQuote",
            "|",
            "bold",
            "italic",
            "fontColor",
            "fontBackgroundColor",
            "removeFormat",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "outdent",
            "indent",
            "|",
            "link",
            "|",
            "imageUpload",
            "mediaEmbed",
            "|",
            "insertTable",
            "|",
            "sourceEditing",
            "maximize",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells", "tableProperties", "tableCellProperties"],
            "tableProperties": {"borderColors": customColorPalette, "backgroundColors": customColorPalette},
            "tableCellProperties": {"borderColors": customColorPalette, "backgroundColors": customColorPalette},
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
            ]
        },
        "htmlSupport": {"allow": [{"name": "/.*/", "attributes": {"id": True}}]},
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        }
    },
}

# Analytics
MATOMO_ID = env("MATOMO_ID", default=None)

# Sentry
SENTRY_DSN = env("SENTRY_DSN", default=None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=1.0,
        send_default_pii=False,
        send_client_reports=False,
    )

# API INSEE
INSEE_API_KEY = env("INSEE_API_KEY", default=None)
INSEE_API_SECRET = env("INSEE_API_SECRET", default=None)
INSEE_API_BASE_URL = "https://api.insee.fr/"
INSEE_TOKEN_API_URL = INSEE_API_BASE_URL + "token/"
INSEE_SIRET_API_URL = INSEE_API_BASE_URL + "entreprises/sirene/V3.11/siret/"

# Custom settings (used by our apps)

# Models to be used with myloaddata/mydumpdata commands
FIXTURE_FOLDER = BASE_DIR / "fixtures"
FIXTURE_MODELS = [
    # Useful Django models
    ("auth", "Permission"),
    ("auth", "Group"),
    # Our models (order matters because of model relations)
    ("data", "User"),
    ("data", "Company"),
    ("data", "SupervisorRole"),
    ("data", "DeclarantRole"),
    ("data", "BlogPost"),
    ("data", "Webinar"),
]
