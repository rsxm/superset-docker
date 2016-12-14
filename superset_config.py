import json
import os

# ---------------------------------------------------------
# Caravel specific config
# ---------------------------------------------------------
ROW_LIMIT = int(os.getenv("ROW_LIMIT", 5000))
WEBSERVER_THREADS = int(os.getenv("WEBSERVER_THREADS", 8))

SUPERSET_WEBSERVER_PORT = int(os.getenv("SUPERSET_WEBSERVER_PORT", 8088))
# ---------------------------------------------------------

# ---------------------------------------------------------
# Flask App Builder configuration
# ---------------------------------------------------------
# Your App secret key
SECRET_KEY = os.getenv("SECRET_KEY", "\2\1thisismyscretkey\1\2\e\y\y\h")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "sqlite:////home/superset/.superset/superset.db")


SUPERSET_ENABLE_PROXY_FIX = True
SUPERSET_AUTH_TYPE = os.getenv("AUTH_TYPE", "REMOTE_USER_AUTH")

# Negated by AUT_REMOTE_USER
SUPERSET_PUBLIC_ROLE_LIKE_GAMMA = False
SUPERSET_ENABLE_CORS = False

if SUPERSET_AUTH_TYPE == "REMOTE_USER_AUTH":
    from flask_appbuilder.security.sqla.manager import SecurityManager
    from flask_appbuilder.security.manager import UserRemoteUserModelView
    from flask_appbuilder.security.sqla.models import User
    from flask_appbuilder.security.manager import AUTH_REMOTE_USER

    class MySecurityManager(SecurityManager):
        user_model = User
        userdbmodelview = UserRemoteUserModelView

    CUSTOM_SECURITY_MANAGER = MySecurityManager
    AUTH_TYPE = AUTH_REMOTE_USER


# Remote user middleware for proxy config:
# http://flask.pocoo.org/snippets/69/
class RemoteUserMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        user = environ.pop('HTTP_REMOTE_USER', None)
        if user:
            environ['REMOTE_USER'] = user

        else:
            if app.config.get('DEBUG'):
                # TODO: Massive data security flaw, only for development!!
                environ['REMOTE_USER'] = 'admin'
            else:
                raise RuntimeError('Check proxy configuration and make sure REMOTE_USER is set correctly.')

        return self.app(environ, start_response)

ADDITIONAL_MIDDLEWARE = [RemoteUserMiddleware, ]


CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "caravel_",
    "CACHE_REDIS_HOST": "redis",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 1,
    "CACHE_REDIS_URL": "redis://redis:6379/1"
}

# Flask-WTF flag for CSRF
CSRF_ENABLED = os.getenv("CSRF_ENABLED", "1") in ("True", "true", "1")

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY", "")

# Whether to run the web server in debug mode or not
DEBUG = os.getenv("DEBUG", "0") in ("True", "true", "1")

# try:
#     CACHE_CONFIG = json.loads(os.getenv("CACHE_CONFIG", "{}"))
# except ValueError:
#     CACHE_CONFIG = {}

# Import all the env variables prefixed with "SUPERSET_"
config_keys = [c for c in os.environ if c.startswith("SUPERSET_")]
for key in config_keys:
    globals()[key[8:]] = os.environ[key]

# This file also allows you to define configuration parameters used by
# Flask App Builder, the web framework used by Caravel. Please consult the
# Flask App Builder Documentation for more information on how to configure
# Caravel: http://flask-appbuilder.readthedocs.org/en/latest/config.html
