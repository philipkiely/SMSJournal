"""
Django settings for SMSJournal project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EFS_ROOT = os.environ['SMSJ_EFS_PATH'] # Where the EFS is mounted, or just a path to the project root locally

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ['SMSJOURNAL_SECRET_KEY'])

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = bool(int(os.environ['SMSJOURNAL_DEBUG_INT'])) # 1 in test, 0 in prod
DEBUG = 0
API_KEY = os.environ['API_KEY']


AWS_PINPOINT_PROJECT_ID = '767e524d9c7542788cebdccfeaa522d9'

ALLOWED_HOSTS = os.environ["SMSJ_ALLOWED_HOSTS"].split(",")
if DEBUG:
    local_ip = str(socket.gethostbyname(socket.gethostname()))
    ALLOWED_HOSTS.append(local_ip)



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'social_django',
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'journals.apps.JournalsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'SMSJournal.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'SMSJournal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['SMSJOURNAL_DB_NAME'],
            'USER': os.environ['SMSJOURNAL_DB_USER'],
            'PASSWORD': os.environ['SMSJOURNAL_DB_PASS'],
            'HOST': os.environ['SMSJOURNAL_DB_HOST'],
            'PORT': os.environ['SMSJOURNAL_DB_PORT'],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1


# Email information
EMAIL_USE_SSL = False
EMAIL_HOST = "mail.hover.com"
EMAIL_HOST_USER = "info@grammiegram.com"
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASS"]
EMAIL_PORT = 587

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = "static"

# Allow CSRF token to be stored in sessions to prevent 403 error with AJAX
CSRF_USE_SESSIONS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}

# social_auth settings
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SMSJOURNAL_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SMSJOURNAL_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/documents']
LOGIN_URL = '/auth/login/google-oauth2'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/'

STRIPE_PRODUCT_ID = "prod_EyHZvJpuEQd2lI"
STRIPE_PLAN_ID = "plan_EyHZXEtvGKZ5oJ"
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
