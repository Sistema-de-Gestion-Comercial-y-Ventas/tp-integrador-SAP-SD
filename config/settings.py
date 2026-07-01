"""
Configuracion principal de Django para el proyecto.

Este archivo define aplicaciones instaladas, middleware, base de datos,
idioma, archivos estaticos y logging.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-t&2tus%r*kr6q&r-ebq%)k2d&e63)q@u0%e4d80ta9c8afd&1$'

DEBUG = True

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    'localhost,127.0.0.1,0.0.0.0,testserver'
).split(',')



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Usa PostgreSQL cuando Docker Compose define las variables DJANGO_DB_*.
# Si no existen esas variables, usa SQLite para desarrollo local simple.

if os.environ.get('DJANGO_DB_ENGINE'):
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DJANGO_DB_ENGINE'),
            'NAME': os.environ.get('DJANGO_DB_NAME'),
            'USER': os.environ.get('DJANGO_DB_USER'),
            'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
            'HOST': os.environ.get('DJANGO_DB_HOST'),
            'PORT': os.environ.get('DJANGO_DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Validacion de contrasenas
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internacionalizacion
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'   # Espanol (Argentina) 

TIME_ZONE = 'America/Argentina/Buenos_Aires' 

USE_I18N = True

USE_TZ = True


# Archivos estaticos (CSS, JavaScript, imagenes)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

# Configuracion de logging
LOGGING = {     
    'version': 1,     
    'disable_existing_loggers': False,     
    'formatters': {         
        'verbose': {             
            'format': '[{levelname}] {asctime} {module} - {message}',             
            'style': '{',         
        },    
    },     
    'handlers': {         
        'console': {             
            'class': 'logging.StreamHandler',             
            'formatter': 'verbose',         
        },     
    },     
    'root': {         
        'handlers': ['console'],         
        'level': 'INFO',     
    }, 
} 
