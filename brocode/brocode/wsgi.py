"""
WSGI config for brocode project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

doteenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(doteenv_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brocode.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
