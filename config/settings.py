"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from dj_database_url import parse as db_url

from decouple import config
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1o_$&(3y!%lykh2vyi*sk5woos0p#3w0nlg+)tehdm=hqq#yz8'

#MAIL
MAIL_SENDER_EMAIL = config("MAIL_SENDER_EMAIL", default="")
MAIL_SENDER_PASSWORD = config("MAIL_SENDER_PASSWORD", default="")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=1, cast=bool)

# All api endpoints start with this name e.g {name}/...
# Except healthcheck.
APIBASE=config("APIBASE", default="demo")

ALLOWED_HOSTS = ["*"]

MEDIA_STORAGE = str(config("MEDIA_STORAGE", default="local")).lower()


FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

CELERY_BROKER_URL = config("REDIS_URL", default="redis://localhost:6379/0")  # or your broker URL
CELERY_RESULT_BACKEND = config("REDIS_URL", default="redis://localhost:6379/0")

CELERY_BEAT_SCHEDULE = {
    'check-bidding-status-every-3-minutes': {
        'task': 'cargo.tasks.check_bidding_status',
        'schedule': crontab(minute='*/3'),
    },
}
redis_url = config("REDIS_URL", default="redis://localhost:6379/0")
REDIS_HOST = str(redis_url).replace("redis://", "").split(":")[0]
REDIS_PORT = int(str(redis_url).replace("redis://", "").split(":")[1].split("/")[0])
REDIS_DB = int(str(redis_url).replace("redis://", "").split(":")[1].split("/")[1])


# Application definition



INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    # .......................
    'mozilla_django_oidc',
    # .......................
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "rest_framework.authtoken",
    'django_celery_beat',
    "accounts",
  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # .......................
    'mozilla_django_oidc.middleware.SessionRefresh',
    # .......................
    #registration middleware
    'cargo.middleware.RegistrationMiddleware',

]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if config("DATABASE_URL", default=None) is not None:
    if len(str(config("DATABASE_URL"))) > 0:
        DATABASES = {
            "default": config(
                "DATABASE_URL",
                default="postgresql://postgres:postgres@localhost:5432/flex-app-template",
                cast=db_url,
            )
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "db.sqlite3",
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = "staticfiles/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

if MEDIA_STORAGE == "cloudinary":
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    import cloudinary_storage

    INSTALLED_APPS += [
        'cloudinary',
        'cloudinary_storage',
    ]

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', ''),
        'API_KEY': config('CLOUDINARY_API_KEY', ''),
        'API_SECRET': config('CLOUDINARY_API_SECRET', ''),
    }

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OIDC SPECIFIC SETTINGS
# Read more here: https://mozilla-django-oidc.readthedocs.io/en/stable/installation.html

AUTHENTICATION_BACKENDS = [
    'config.auth.OIDCAuthenticationBackend',
    # 'django.contrib.auth.backends.ModelBackend'
]

AUTH_USER_MODEL = 'accounts.User'
# rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=250),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# OpenID Connect
OIDC_RP_SIGN_ALGO = "RS256"
#
OIDC_RP_CLIENT_ID = config('OIDC_RP_CLIENT_ID', default="")
OIDC_RP_CLIENT_SECRET = config('OIDC_RP_CLIENT_SECRET', default="")

OIDC_OP_AUTHORIZATION_ENDPOINT = config('OIDC_OP_AUTHORIZATION_ENDPOINT', default="")
OIDC_OP_TOKEN_ENDPOINT = config("OIDC_OP_TOKEN_ENDPOINT", default="")
OIDC_OP_USER_ENDPOINT = config("OIDC_OP_USER_ENDPOINT", default="")
OIDC_OP_JWKS_ENDPOINT = config("OIDC_OP_JWKS_ENDPOINT", default="")
OIDC_OP_END_SESSION_ENDPOINT = config("OIDC_OP_END_SESSION_ENDPOINT", default="")

#channels configuration
CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
           # read from env first
           "hosts": [config("REDIS_URL", default="redis://localhost:6379")],
        },
    },
}