from .common import *
from agregator_ofd.settings import db_config

DEBUG = True

SSL = True

DATABASES = {
    "default": db_config.TEST_SETTINGS
}

ALLOWED_HOSTS = ['']

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')