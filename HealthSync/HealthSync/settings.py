"""
Django settings for HealthSync project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bi38)g5d%ry^z%e1bgq@mwc^c93s2%()oin_g(d&80p%&%m7b1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'core',
    'jazzmin',
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
]

ROOT_URLCONF = 'HealthSync.urls'

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

WSGI_APPLICATION = 'HealthSync.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# URL to access static files, should end with a slash
STATIC_URL = '/static/'

# Sets default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Directory where Django will collect all static files for deployment (used during production)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional locations of static files (for development)
STATICFILES_DIRS = [
    BASE_DIR / "core/static"  # Directory for additional static files during development
]

import os  # Importing os module for path manipulations

# URL to access media files, should end with a slash
MEDIA_URL = '/media/'

# Directory for uploaded media files (e.g., user uploads, profile pictures)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL to redirect to after a user logs out
LOGOUT_REDIRECT_URL = 'request_otp'

# Email configuration for sending emails via SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Specifies SMTP as the email backend
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'  # Host for the SMTP server
EMAIL_PORT = 2525  # Port for the SMTP server
EMAIL_HOST_USER = '61eb56a914b7eb'  # Username for the SMTP server
EMAIL_HOST_PASSWORD = '41d1ab55876a88'  # Password for the SMTP server
EMAIL_USE_TLS = True  # Enables TLS encryption for email transmission
DEFAULT_FROM_EMAIL = 'noreply@healthsync.com'  # Default "From" email address for outgoing emails


JAZZMIN_SETTINGS = {
    "site_header": "HealthSync Admin Panel",
    "site_brand": "Admin",
    "site_logo": "img/Healthsync-B.png",
    "site_logo_classes": "img-square rounded",
    "welcome_sign": "Welcome to HealthSync Admin Panel!",
    "site_footer": "HealthSync © 2024",
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["core.Profile", "core.Order", "core.OrderItem", "core.Donation", "core.Product", "core.Manufacturer","core.BloodDonor", "core.PharmacyRegistration"],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-user-shield",
        "core.BloodDonor": "fas fa-hand-holding-medical",
        "core.Donation": "fas fa-heartbeat",
        "core.Manufacturer": "fas fa-industry",
        "core.Order": "fas fa-shopping-cart",
        "core.OrderItem": "fas fa-box-open",
        "core.PharmacyRegistration": "fas fa-hospital-user",
        "core.Product": "fas fa-pills",
        "core.Profile": "fas fa-id-card",


    },

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "core"},
    ],

    "usermenu_links": [
        {"name": "Home", "url": "/", "new_window": True, "icon": "fas fa-home"},
        {"name": "Doctors", "url": "/doctors/", "new_window": True, "icon": "fas fa-user-md"},
        {"name": "Medicine", "url": "/medicine/", "new_window": True, "icon": "fas fa-pills"},
        {"name": "Donors", "url": "/blood-donors/", "new_window": True, "icon": "fas fa-hand-holding-medical"},

    ],

    "changeform_format": "collapsible",
    "changeform_format_overrides": {
        "auth.user": "horizontal_tabs",
    },
}
