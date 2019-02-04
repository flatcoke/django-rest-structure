"""
WSGI config for flatcoke project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import dotenv
import os
from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                '.env'))
f = open('.env_example', 'r')
for i in f.readlines():
    if os.environ.get(i.rstrip()) is None:
        raise EnvironmentError('must set env in list of env_example file')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flatcoke.settings.development")

application = get_wsgi_application()
