# Django settings for unit test project.
import os
import sys

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'filer_addons/tests/database.sqlite',
    },
}

SITE_ID = 1

ROOT_URLCONF = 'filer_addons.tests.testapp.urls'

SECRET_KEY = 'secret'

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, APP_ROOT + "/../")

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/static/'

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'filer_addons',
    'filer_addons.filer_gui',
    'filer_addons.filer_signals',
    'filer_addons.tests.testapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
