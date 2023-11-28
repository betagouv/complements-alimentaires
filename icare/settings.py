"""
Django settings for icare project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import sys
import os
import dotenv  # noqa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET")
SECURE_SSL_REDIRECT = os.getenv("FORCE_HTTPS") == "True"

SECURE = os.getenv("SECURE") == "True"
PROTOCOL = "https" if SECURE else "http"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"
AUTH_USER_MODEL = "data.User"

ALLOWED_HOSTS = [x.strip() for x in os.getenv("ALLOWED_HOSTS").split(",")]

ENVIRONMENT = os.getenv("ENVIRONMENT")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "webpack_loader",
    "ckeditor",
    "ckeditor_uploader",
    "anymail",
    "icare",
    "api",
    "data",
    "web",
    "simple_history",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

CSRF_COOKIE_NAME = "csrftoken"
ROOT_URLCONF = "icare.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "icare.wsgi.application"

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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.getenv("DB_USER"),
        "NAME": os.getenv("DB_NAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "CONN_MAX_AGE": 60,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

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
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media and file storage
DEFAULT_FILE_STORAGE = os.getenv("DEFAULT_FILE_STORAGE")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

STATICFILES_STORAGE = os.getenv("STATICFILES_STORAGE")
SESSION_COOKIE_AGE = 31536000
SESSION_COOKIE_SECURE = os.getenv("SECURE") == "True"
SESSION_COOKIE_HTTPONLY = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/s-identifier"

HOSTNAME = os.getenv("HOSTNAME")

# Email
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")

if DEBUG and EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025

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

NEWSLETTER_BREVO_LIST_ID = os.getenv("NEWSLETTER_BREVO_LIST_ID")
ANYMAIL = {
    "SENDINBLUE_API_KEY": os.getenv("BREVO_API_KEY", ""),
}

# CK Editor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format", "Blockquote"],
            ["Bold", "Italic"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
            ],
            ["Link", "Unlink"],
            [
                "Image",
                "-",
                "Table",
                "SpecialChar",
            ],
            ["Source", "Maximize"],
        ],
        "extraPlugins": ",".join(
            [
                "image2",
                "codesnippet",
                "placeholder",
            ]
        ),
        "removePlugins": ",".join(["image"]),
    }
}
