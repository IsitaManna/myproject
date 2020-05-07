"""
Django settings for Biloba project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!@1!8*!=42okri%&j_&^0cor1)%!6z18u1i%l%e+$%)$nnbpoa'

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('MODE') == 'Prod':
    DEBUG = False
else:
    DEBUG = True

# ALLOWED_HOSTS = ["192.168.1.10", "localhost", "192.168.1.100","192.168.1.13"]
ALLOWED_HOSTS = "*"


# Application definition

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


INSTALLED_APPS = [
    'corsheaders',
    'recommendationEngine.apps.recommendationEngineConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'Biloba.urls'

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

WSGI_APPLICATION = 'Biloba.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
        'NAME' : os.getenv('MYSQL_DB'),
        'USER' : os.getenv('MYSQL_USER'),
        'PASSWORD' : os.getenv('MYSQL_PASS'),
        'HOST' : os.getenv('MYSQL_HOST'),
        'PORT' : '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'recommendationEngine.User'


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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Logging configs

if DEBUG:
    LOG_PATH = f'{BASE_DIR}/dev_logs/django-laiout.log'
else:
    LOG_PATH = f'{os.getenv("LOG_DIR")}/django-laiout.log'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_PATH,
            'backupCount': 7,
            'when': 'D',
            'interval': 1,
            'utc': False,
            'encoding': None,
            'formatter': 'simple'

        },
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'] if DEBUG else ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'] if DEBUG else ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.security.*': {
            'handlers': ['console', 'file'] if DEBUG else ['file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}



OCR_IMAGE_DIR = '/home/tebackup/Workspace/Laiout/floor_plans/' # absolute path

GAN_PREDICT_IMAGE_DIR = "/media/gan_test_img/" # relative path

PLAN_COLOR_DICT = [{'Floor tags': 'balcony/ porch', 'R': 77, 'G': 11, 'B': 65},
                {'Floor tags': 'bath', 'R': 2, 'G': 190, 'B': 242},
                {'Floor tags': 'bedroom', 'R': 163, 'G': 242, 'B': 17},
                {'Floor tags': 'bonus', 'R': 247, 'G': 231, 'B': 186},
                {'Floor tags': 'closet', 'R': 18, 'G': 102, 'B': 3},
                {'Floor tags': 'deck/outdoor space', 'R': 181, 'G': 166, 'B': 66},
                {'Floor tags': 'den', 'R': 250, 'G': 214, 'B': 165},
                {'Floor tags': 'dining room', 'R': 189, 'G': 185, 'B': 185},
                {'Floor tags': 'door', 'R': 245, 'G': 66, 'B': 242},
                {'Floor tags': 'entry', 'R': 28, 'G': 35, 'B': 145},
                {'Floor tags': 'firepit/fireplace', 'R': 255, 'G': 117, 'B': 24},
                {'Floor tags': 'garage', 'R': 130, 'G': 102, 'B': 68},
                {'Floor tags': 'hot tub', 'R': 228, 'G': 155, 'B': 15},
                {'Floor tags': 'kitchen/living room', 'R': 250, 'G': 233, 'B': 137},
                {'Floor tags': 'kitchen', 'R': 171, 'G': 24, 'B': 240},
                {'Floor tags': 'laundry', 'R': 245, 'G': 137, 'B': 5},
                {'Floor tags': 'living room', 'R': 17, 'G': 93, 'B': 245},
                {'Floor tags': 'mudroom', 'R': 112, 'G': 66, 'B': 20},
                {'Floor tags': 'office', 'R': 255, 'G': 0, 'B': 255},
                {'Floor tags': 'pantry', 'R': 252, 'G': 83, 'B': 83},
                {'Floor tags': 'stair', 'R': 229, 'G': 192, 'B': 240},
                {'Floor tags': 'storage', 'R': 245, 'G': 173, 'B': 91},
                {'Floor tags': 'sunroom', 'R': 227, 'G': 11, 'B': 93},
                {'Floor tags': 'utility', 'R': 166, 'G': 66, 'B': 0},
                {'Floor tags': 'WIC', 'R': 191, 'G': 148, 'B': 228},
                {'Floor tags': 'window', 'R': 227, 'G': 69, 'B': 30},
                {'Floor tags': 'master bedroom', 'R': 98, 'G': 98, 'B': 30},
                {'Floor tags': 'living/ dining', 'R': 40, 'G': 60, 'B': 90},
                {'Floor tags': 'kitchen/dining', 'R': 100, 'G': 80, 'B': 120},
                {'Floor tags': 'hall', 'R': 63, 'G': 72, 'B': 204},
                {'Floor tags': 'linen', 'R': 225, 'G': 175, 'B': 166},
                {'Floor tags': 'Misc/cinema', 'R': 34, 'G': 177, 'B': 76}]