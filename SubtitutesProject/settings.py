"""
Django settings for SubtitutesProject project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import json
import os

from django.utils.translation import gettext_lazy as _
from pathlib import Path
from dotenv import load_dotenv
from os import environ
load_dotenv()
from django.core.management.utils import get_random_secret_key

# from django.urls import reverse
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('DJANGO_SECRET_KEY',get_random_secret_key())
DEBUG = environ.get('DJANGO_DEBUG', '') != 'False'
DEVELOPMENT_MODE = False
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ["*"]

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

# Application definition

INSTALLED_APPS = [
    'constance',
    'timetable.apps.TimetableConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

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

CONSTANCE_CONFIG = {
    'ADDING_STUDENTS':(False,"Weather Student Creation is enabled or disabled",bool),
}

ROOT_URLCONF = 'SubtitutesProject.urls'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'subs',
        'USER': environ['DB_USER'],
        'PASSWORD': environ['DB_PASSWORD'],
        'HOST': environ['DB_HOST'],
        'PORT': environ['DB_PORT'],
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

LANGUAGE_CODE = 'he'

TIME_ZONE = 'Asia/Jerusalem'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static_output'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/teacher/home"
LOGIN_URL = '/teacher/user/login'
AUTH_USER_MODEL = 'timetable.Teacher'
LOGOUT_REDIRECT_URL = '/teacher/user/login'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = environ['EMAIL_HOST']
EMAIL_USE_TLS = True
EMAIL_PORT = environ['EMAIL_PORT']
EMAIL_HOST_USER = environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = environ['DEFAULT_FROM_EMAIL']

# translation
LANGUAGES = (
    ('he', _('Hebrew')),
    ('en', _('English')),
)
LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]
CSRF_TRUSTED_ORIGINS = json.loads(environ["CSRF_TRUSTED_ORIGINS"])
X_FRAME_OPTIONS = 'SAMEORIGIN'
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

LAPTOPS_ENABLED = environ.get('LAPTOPS_ENABLED', False)
print(LAPTOPS_ENABLED)
if LAPTOPS_ENABLED == "True":
    LAPTOPS_ENABLED=True
else:
    LAPTOPS_ENABLED = False
if LAPTOPS_ENABLED:
    CONSTANCE_CONFIG['LAPTOPS'] = (0,"Number Of Laptops Available (CHANGING THIS REQUIRES RESTARTING)",int)
    INSTALLED_APPS += 'LaptopLoaning.apps.LaptoploaningConfig',
if environ.get("SLACK_BOT_TOKEN"):
    SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")

DASHBOARD_ENABLED = environ.get('DASHBOARD_ENABLED', False)
if DASHBOARD_ENABLED == "True":
    DASHBOARD_ENABLED =True
else:
    DASHBOARD_ENABLED = False
if DASHBOARD_ENABLED:
    INSTALLED_APPS += 'dashboard',
