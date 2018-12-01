try:
    from flatcoke.settings.base import *
except ImportError:
    pass

DEBUG = False
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
)
