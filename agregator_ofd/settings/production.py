from .common import *
from agregator_ofd.settings import db_config

DEBUG = False

SSL = True

DATABASES = {
    "default": db_config.PRODUCTION_SETTINGS
}



STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')