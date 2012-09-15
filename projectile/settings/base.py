# -*- coding: utf-8 -*-

import os
#import memcache_toolbar.panels.memcache

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'base_css': (
            'css/style.css',
        ),
    },
    'js': {
        'libs_js': (
            'js/libs/jquery-1.6.2.min.js',
            'js/libs/modernizr-2.0.6.min.js',
        ),
    }
}

SUPPORTED_NONLOCALES = ['media', 'admin', 'static']

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
    )

SITE_ID = 1
ROOT_URLCONF = 'projectile.urls'

REFERENCE_NAME = 'projectile'
INSTALLED_APPS = [
    # Template apps
    #'jingo_minify',

    # Django contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.humanize',
    'django.contrib.syndication',
    'django.contrib.staticfiles',

    # Third-party apps, patches, fixes
#    'django_nose',
    'session_csrf',
    'debug_toolbar',
    'treebeard',
#    'pagination',
#    'widget_tweaks',
    'crispy_forms',
    #'debug_toolbar_user_panel',
    #'memcache_toolbar',

    # Database migrations
    'south',

    # Application base, containing global templates.
    'projectile.baseapp',

    # Local apps, referenced via REFERENCE_NAME.appname
]

# Place bcrypt first in the list, so it will be the default password hashing
# mechanism
PASSWORD_HASHERS = (
#    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = True

# Set this to true if you are using https
SESSION_COOKIE_SECURE = False

## Tests
TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# django-pagination config
PAGINATION_DEFAULT_PAGINATION = 5
PAGINATION_DEFAULT_WINDOW = 2

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    #'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',
    #'jingo_minify.helpers.build_ids',
]

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)
TEMPLATE_LOADERS = (
#    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
)


def custom_show_toolbar(request):
    return False


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': True,
    'TAG': 'body',
    'SHOW_TEMPLATE_CONTEXT': True,
    'ENABLE_STACKTRACES': True,
}

DEBUG_TOOLBAR_PANELS = (
    #'debug_toolbar_user_panel.panels.UserPanel',
    #'memcache_toolbar.panels.memcache.MemcachePanel',
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

# Specify a model to use for user profiles, if desired.
#AUTH_PROFILE_MODULE = 'c300.accounts.UserProfile'

FILE_UPLOAD_PERMISSIONS = 0664

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
#JINGO_EXCLUDE_APPS = [
#    'admin',
#    'registration',
#    'debug_toolbar',
#    'debug_toolbar_user_panel',
#    'memcache_toolbar',
#]

# The WSGI Application to use for runserver
#WSGI_APPLICATION = 'c300.wsgi.application'

CUSTOM_USER_MODEL = 'projectile.consumers.ConsumerProfile'
LOGIN_URL = '/baseapp/login/'

AUTH_PROFILE_MODULE = 'projectile.consumers.ConsumerProfile'
AUTHENTICATION_BACKENDS = [
    'projectile.consumers.ConsumerBackend',
    'django.contrib.auth.backends.ModelBackend',
]
