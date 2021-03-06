"""
Django settings for FlirtAPI project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# noinspection SpellCheckingInspection
SECRET_KEY = '+y@qd8ycpejfm(a98!uvb6l38#t5gh8kcfhor^k%+4w8j-4w8&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'flirtapi-test.herokuapp.com',
    'storage.googleapis.com/optimal-card-137823.appspot.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web_api.apps.WebApiConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',	
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'FlirtAPI.urls'

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

WSGI_APPLICATION = 'FlirtAPI.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Local database
# # noinspection SpellCheckingInspection
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'flirt_app_db',  # os.path.join(BASE_DIR, 'db.sqlite3'),
#         'USER': 'flirt_app_dev',
#         'PASSWORD': 'devpass',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Heroku database
# noinspection SpellCheckingInspection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd5g1skeikuok7s',  # os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': 'tfwibsgxmmrxmv',
        'PASSWORD': '-gvNsIkBylR0rXq17cEqvxKN0H',
        'HOST': 'ec2-54-221-240-149.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# REPOSITORY_ROOT = os.path.dirname(BASE_DIR)

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(REPOSITORY_ROOT, 'static')

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'media')

CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

# Google Places API settings
PLACES_API_KEY = 'AIzaSyDno48GdzMu5mM6NXOVjT4DypNmBV2QnKA'
PLACES_SEARCH_RADIUS = 75

# Firebase cloud messaging settings
FIREBASE_API_KEY = 'AIzaSyDHVCPltI_zsZUsZoZb9gJyac79rIYAx1s'
FIREBASE_SEND_URL = 'https://fcm.googleapis.com/fcm/send'

PREPEND_WWW = False

LIBCLOUD_PROVIDERS = {
    'google_cloud_storage': {
        'type': 'libcloud.storage.types.Provider.GOOGLE_STORAGE',
        'user': 'GOOGXZH7J5JF5Y7G6YFZ', # 'optimal-card-137823',
        'key': '43MseYADBAyPfvk/hUFtCnVDnP+pMUzXZWaBeu1z', # 'AIzaSyDHVCPltI_zsZUsZoZb9gJyac79rIYAx1s',
        'bucket': 'optimal-card-137823.appspot.com',
        'secure': True,
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'

STATIC_ROOT = 'https://storage.googleapis.com/optimal-card-137823.appspot.com'
STATIC_URL = '/'
SELFIE_URL = 'selfies'
STATICFILES_STORAGE = 'djlibcloud.storage.LibCloudStorage'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = []

# Added for compression and caching
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Set cloud storage as default
STATICFILES_STORAGE = 'djlibcloud.storage.LibCloudStorage'
DEFAULT_FILE_STORAGE = 'djlibcloud.storage.LibCloudStorage'
DEFAULT_LIBCLOUD_PROVIDER = 'google_cloud_storage'
