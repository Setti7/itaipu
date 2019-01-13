"""
Django settings for itaipu project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import json
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Importing envvars from env.json:
def get_envvar(var, alt=None):
    with open('setup/env.json', 'r') as f:
        data = json.loads(f.read())
        return data.get(var, alt)


def gen_SECRET_KEY():
    import random
    SECRET_KEY = ''.join(
        [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

    with open('setup/env.json', 'r') as f:
        data = json.loads(f.read())

    with open('setup/env.json', 'w') as f:
        data['SECRET_KEY'] = SECRET_KEY

        f.write(json.dumps(data, indent=4))


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

    'debug_toolbar',

    'contas.apps.ContasConfig',
    'core.apps.CoreConfig',

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

    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Django Toolbar config
# https://github.com/jazzband/django-debug-toolbar

INTERNAL_IPS = ['127.0.0.1']

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = '/contas/login'
LOGIN_REDIRECT_URL = '/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30


# Sentry config
# https://sentry.io/

sentry_sdk.init(
    dsn="https://2893784632054e68a96704f984638966@sentry.io/1354523",
    integrations=[DjangoIntegration()]
)


# Email settings
# https://app.sendgrid.com/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DOMAIN = get_envvar('DOMAIN')
EMAIL_ADMIN = "Administrador admin@%s" % DOMAIN
EMAIL_ADMIN_SHOW = "admin@%s" % DOMAIN

DEFAULT_FROM_EMAIL = 'Não Responda não-responda@%s' % DOMAIN
ACCOUNT_RECOVERY_EMAIL = 'Redefinir Senha redefinir-senha@%s' % DOMAIN
REGISTRATION_EMAIL = 'Bem-Vindo novos-moradores@%s' % DOMAIN

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = get_envvar('SENDGRID_API_KEY')
EMAIL_USE_TLS = True
EMAIL_PORT = 587


## Descomente caso esteja com SSL

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
