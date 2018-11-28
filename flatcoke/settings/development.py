import sys

try:
    from flatcoke.settings.base import *
except ImportError:
    pass

DEBUG = True

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    pass
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }
