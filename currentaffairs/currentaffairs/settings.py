"""
Django settings for currentaffairs project.
Production-ready version.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# ENV
# =========================

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-me-in-production"
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',

    # Local apps
    'users',
    'core',
    'topics',
    'comments',
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'currentaffairs.urls'


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'currentaffairs.wsgi.application'


# =========================
# DATABASE
# =========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================
# AUTH
# =========================

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'


# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('be', _('Беларуская')),
    ('en', _('English')),
    ('it', _('Italiano')),
    ('lt', _('Lietuviu')),
    ('ru', _('Русский')),
    ('ua', _('Українська')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# =========================
# STATIC / MEDIA
# =========================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# important for  production
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =========================
# SECURITY
# =========================

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# =========================
# LOGGING
# =========================

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {message}",
#             "style": "{",
#         },
#     },
#
#     "handlers": {
#         "file": {
#             "level": "WARNING",
#             "class": "logging.FileHandler",
#             "filename": LOGS_DIR / "django.log",
#             "formatter": "verbose",
#         },
#     },
#
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "WARNING",
#             "propagate": True,
#         },
#     },
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "django.log",
        },
    },
    "loggers": {
        "django.contrib.sessions": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
        },
        "django.security": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
        },
    },
}

# =========================
# DEFAULT PK
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
