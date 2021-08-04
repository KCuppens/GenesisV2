"""
Django settings for GenesisV2 project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from django.contrib import messages
from pathlib import Path
import os 
from decouple import config
from django.utils.translation import ugettext_lazy as _
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = ['localhost', '127.0.0.1','46.101.244.242']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)
# AUTH_USER_MODEL = "user.User"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    #third-party apps
    'widget_tweaks',
    'translation_manager',
    'modeltranslation',
    'compressor',
    'tags_input',

    #apps
    'apps.blocks', 
    'apps.conf',
    'apps.base',
    'apps.dashboard',
    'apps.user',
    'apps.account',
    'apps.history',
    'apps.modules',
    'apps.feathericons',
    'apps.translation',
    'apps.pages',
    'apps.filemanager',
    'apps.logs',
    'apps.front',
    'apps.search',
    'apps.data',
    'apps.news',
    'apps.mail',
    'apps.formbuilder',
]

AUTH_USER_MODEL = "user.User"

TAGS_INPUT_INCLUDE_JQUERY = True

def get_queryset(*args, **kwargs):
    from apps.filemanager.models import Media
    return Media.objects.all()

TAGS_INPUT_MAPPINGS = {
    'base.Tags': 
        {
            'field': 'file'
        }
}

TRANSLATABLE_MODEL_MODULES = []

TEMPLATE_ENGINE = 'django'
SENDING_ORDER = ['-priority']
LOG_LEVEL = '2'
DEFAULT_PRIORITY = 'medium'
THREADS_PER_PROCESS = '5'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'apps.base.middleware.RedirectMiddleware'
]

ROOT_URLCONF = 'GenesisV2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #topnav
                'apps.dashboard.context_processors.topnav.get_topnav',
                #front
                'apps.front.context_processors.pages.get_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'GenesisV2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DEV_DB_NAME'),
        'USER': config('DEV_DB_USER'),
        'PASSWORD': config('DEV_DB_PASSWORD'),
        'HOST': config('DEV_DB_HOST'),
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "nl"
MODELTRANSLATION_LANGUAGES = ('nl', 'en', 'fr')
LANGUAGES = [
    ('nl', _('Nederlands')),
    ('en', _('Engels')),
    ('fr', _('Frans'))
]
TRANSLATIONS_BASE_DIR = BASE_DIR
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'nl'

TIME_ZONE = "Europe/Brussels"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# customising 'include/messages' tags

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_ROOT = os.path.join(BASE_DIR, 'new_static')
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
IMAGES_DIR = os.path.join(MEDIA_ROOT, 'images')
COMPRESS_STORAGE = 'compressor.storage.CompressorFileStorage'
COMPRESS_ENABLED = True
STATICFILES_STORAGE = 'GenesisV2.storage.WhiteNoiseStaticFilesStorage'

# for exact login view
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'
MAILJET_API_KEY = 'a8ed2ad7a17b71d57b440c4ddc0022ce'
MAILJET_API_SECRET = '6868b478558189199dcfdde021236066'
BACKENDS = ''
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER ='Your email name'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = "Don't Reply<noreply@mydomain.com>"
# EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'App password from google'
#Logging
# import logging

# versions older than VERSION_DELETE_DAYS will be deleted
VERSION_DELETE_DAYS = 15

SITE_ID=1

GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS')
GOOGLE_PROPERTY_ID = config('GOOGLE_PROPERTY_ID')

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

