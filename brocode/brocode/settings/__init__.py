import os
from .base import *
from django.conf import settings

'''
APP_ENV environment variable which we have to mention in our .env file
used for settings like dev.py and stage.py
'''
if os.getenv('APP_ENV') == 'prod':
    from .prod import *
else:
    from .dev import *