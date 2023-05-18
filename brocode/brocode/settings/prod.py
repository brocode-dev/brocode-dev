

import os


DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME':  os.getenv('DB_NAME'),
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host': os.getenv('HOST')
            }  
        },
        'TEST': {
            'ENGINE': 'djongo',
            'NAME':  'test_goldloancollateral',
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host': os.getenv('HOST')
            }  
        }
}


