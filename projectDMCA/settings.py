"""
Django settings for projectDMCA project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5nr-4-(4id&)c)7q%+if((6rm%e+h&un)gyq)&p(yo_zsl688!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'gdstorage',
    # 'cloudinary',
    'phonenumber_field',
    'taggit',
    # custom applications
    'account.apps.AccountConfig',
    'administrator.apps.AdministratorConfig',
    'announcement.apps.AnnouncementConfig',
    'grading_system.apps.GradingSystemConfig',
    'accounting_transaction.apps.AccountingTransactionConfig',
    'admission.apps.AdmissionConfig',
]

AUTH_USER_MODEL = 'account.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projectDMCA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'account/templates'),
            os.path.join(BASE_DIR, 'account/templates/account'),
            os.path.join(
                BASE_DIR, 'account/templates/account/registration'),
            os.path.join(BASE_DIR, 'administrator/templates'),
            os.path.join(BASE_DIR, 'announcement/templates'),
            os.path.join(BASE_DIR, 'grading_system/templates/student'),
            os.path.join(BASE_DIR, 'grading_system/templates/faculty'),
            os.path.join(BASE_DIR, 'accounting_transaction/templates'),
            os.path.join(BASE_DIR, 'admission/templates'),
        ],
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

WSGI_APPLICATION = 'projectDMCA.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
        'NAME': 'dmcadb',
        'USER': 'pypert',
        'PASSWORD': 'P@ssw0rd',
        'HOST': '127.0.0.1',
        'PORT': ''
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

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static/img')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'account:dashboard'
LOGOUT_REDIRECT_URL = 'login'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'web.dmca.noreply@gmail.com'
EMAIL_HOST_PASSWORD = 'dmcawebte@m'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PHONENUMBER_DEFAULT_REGION = 'PH'
# GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(
# BASE_DIR, 'dmca-bataan-5db059fab413.json')
# cloudinary.config(cloud_name='drkokcmbv',
#                  api_key='244943981247488',
#                  api_secret='irZIkeUt4pXlDkd1lG1jT3p427Q')
# django_heroku.settings(locals())
