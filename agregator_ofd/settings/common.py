"""
Django settings for agregator_ofd project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, '../')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("APPLICATION_SECRET_KEY", 'tw8w$m^s-6qw(uol7^j9qlu+t4@p28ceb+()o&m%sxj62*%o#x')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# apps added from libraries
BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # not standard django apps
    # swagger - generating html views fro backend
    'drf_yasg'

]

# local apps in this project
ADDITIONAL_APPS = [
    'core',
]

# installed apps separated to apps from libs, and locally created ones
INSTALLED_APPS = BASE_APPS + ADDITIONAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'agregator_ofd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
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
"""
DB Configuration
If Production in evnironment, use production 
db passes
"""

WSGI_APPLICATION = 'agregator_ofd.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Statics
STATIC_URL = '/static-agregator/'

# Media
MEDIA_URL = '/media-agregator/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# AUTH CONFIGURATION
AUTH_USER_MODEL = 'core.CustomUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
