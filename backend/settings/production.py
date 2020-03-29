from .base import *

DEBUG = False

IMAGES_FOLDER = "images/"
CATALOGS_FOLDER = "catalogs/"

try:
    from .special_settings import DATABASES_SETTINGS
    from .special_settings import DROPBOX_ACCESS_TOKEN
    from .special_settings import EMAIL_HOST_PASSWORD
    from .special_settings import EMAIL_HOST_USER
    from .special_settings import SERVER_URL
except:
    DATABASES_SETTINGS = {}
    DROPBOX_ACCESS_TOKEN = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_HOST_USER = ""
    SERVER_URL = ""

DATABASES = {
    'default': DATABASES_SETTINGS
}

SITE_URL = "{}".format(SERVER_URL)
SITE_URL_ROOT = "http://{}".format(SITE_URL)

BACKEND_URL = "{}:81".format(SERVER_URL)
BACKEND_URL_ROOT = "http://{}".format(BACKEND_URL)

CORS_ORIGIN_WHITELIST = (
       SITE_URL_ROOT,
)

ENVIRONMENT = "production"

DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': DROPBOX_ACCESS_TOKEN,
}


MIGRATION_MODULES = {}
