"""
Django settings for itaipu project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from .utils import get_envvar
from .logging_filters import skip_media_requests, skip_static_requests

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_envvar('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_envvar('DEBUG')

ALLOWED_HOSTS = get_envvar('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [

    'tinymce',

    'contas.apps.ContasConfig',
    'core.apps.CoreConfig',
    'avisos.apps.AvisosConfig',

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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'itaipu.middleware.UserBasedExceptionMiddleware',

]

ROOT_URLCONF = 'itaipu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'contas.context_processors.constants_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'itaipu.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_envvar('db_name', 'itaipu'),
        'USER': get_envvar('db_user', 'itaipu-web'),
        'PASSWORD': get_envvar('db_password', 'escolha uma senha'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'contas.Residente'

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

# Logging that filters media and static calls
# https://stackoverflow.com/questions/23833642/django-how-to-filter-out-get-static-and-media-messages-with-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        # use Django's built in CallbackFilter to point to your filter
        'skip_static_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_static_requests
        },
        'skip_media_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_media_requests
        }
    },
    'formatters': {
        # django's default formatter
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        # django's default handler
        'django.server': {
            'level': 'INFO',
            'filters': ['skip_static_requests', 'skip_media_requests'],
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        # django's default logger
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Django Toolbar config
# https://github.com/jazzband/django-debug-toolbar

INTERNAL_IPS = ['127.0.0.1']

# TinyMCE configuration
# from: https://pythonprogramming.net/admin-apps-django-tutorial/

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/contas/login'
LOGIN_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

# Email settings
# https://docs.djangoproject.com/en/2.1/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_ADMIN = 'correioparqueitaipu@gmail.com'
EMAIL_ADMIN_SHOW = 'correioparqueitaipu@gmail.com'

DEFAULT_FROM_EMAIL = 'correioparqueitaipu@gmail.com'
ACCOUNT_RECOVERY_EMAIL = 'correioparqueitaipu@gmail.com'
REGISTRATION_EMAIL = 'correioparqueitaipu@gmail.com'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'correioparqueitaipu@gmail.com'
EMAIL_HOST_PASSWORD = 'gy761qaA'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

if DEBUG:

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    #     }
    # }

else:

    # Sentry config
    # https://sentry.io/

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn="https://2893784632054e68a96704f984638966@sentry.io/1354523",
        integrations=[DjangoIntegration()]
    )

    ## Descomente caso esteja com SSL

    # SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_BROWSER_XSS_FILTER = True
    # SECURE_SSL_REDIRECT = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    # X_FRAME_OPTIONS = 'DENY'
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
