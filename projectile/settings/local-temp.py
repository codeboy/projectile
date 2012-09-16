# -*- coding: utf-8 -*-
"""
This is an example settings/local.py file.
These settings overrides what's in settings/base.py
"""

import logging

# To extend any settings from settings/base.py here's an example:
#from . import base
#INSTALLED_APPS = base.INSTALLED_APPS + ['debug_toolbar']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'projectile',
        'USER': 'projectile',
        'PASSWORD': 'Cj405kw7H2b5KW',
        'HOST': '127.0.0.1',
#        'PORT': '5432',
        }
}


# Uncomment this and set to all slave DBs in use on the site.
# SLAVE_DATABASES = ['slave']

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Moscow'

# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = TEMPLATE_DEBUG = True

# Is this a development instance? Set this to True on development/master
# instances and False on stage/prod.
DEV = True

SECRET_KEY = '_^(m436@a$omj4(4(-xep&!0&i-%c4#^ag55!(m9%nsnta=66a'

# Uncomment these to activate and customize Celery:
# CELERY_ALWAYS_EAGER = False  # required to activate celeryd
# BROKER_HOST = 'localhost'
# BROKER_PORT = 5672
# BROKER_USER = 'django'
# BROKER_PASSWORD = 'django'
# BROKER_VHOST = 'django'
# CELERY_RESULT_BACKEND = 'amqp'

## Log settings

LOG_LEVEL = logging.INFO
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_c300"  # Make this unique to your project.
# Remove this configuration variable to use your custom logging configuration
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'loggers': {
        'c300': {
            'level': "DEBUG"
        }
    }
}

# Common Event Format logging parameters
#CEF_PRODUCT = 'c300'
#CEF_VENDOR = 'Your Company'
#CEF_VERSION = '0'
#CEF_DEVICE_VERSION = '0'

INTERNAL_IPS = ('127.0.0.1')

# Enable these options for memcached
#CACHE_BACKEND= "memcached://127.0.0.1:11211/"
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True

# Set this to true if you use a proxy that sets X-Forwarded-Host
#USE_X_FORWARDED_HOST = False

SERVER_EMAIL = "webmaster@example.com"
DEFAULT_FROM_EMAIL = "webmaster@example.com"
SYSTEM_EMAIL_PREFIX = "[c300]"
