from .base import *

DEBUG = True

IMAGES_FOLDER = "dev/images/"
CATALOGS_FOLDER = "dev/catalogs/"


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

DATABASES_SETTINGS['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': DATABASES_SETTINGS
}

SITE_URL = "{}:3000".format(SERVER_URL)
SITE_URL_ROOT = "http://{}".format(SITE_URL)

BACKEND_URL = "{}:5000".format(SERVER_URL)
BACKEND_URL_ROOT = "http://{}".format(BACKEND_URL)

CORS_ORIGIN_WHITELIST = (
       SITE_URL_ROOT,
)

ENVIRONMENT = "development"

DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': DROPBOX_ACCESS_TOKEN,
}

# MIGRATION_MODULES = dict([(app, 'migrations') for app in INSTALLED_APPS])

LOGGING = {}