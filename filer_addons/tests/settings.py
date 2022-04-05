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

APP_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..")
)
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        '..'
    )
)

sys.path.insert(0, APP_ROOT + "/../")

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

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

INSTALLED_APPS = [
    # 'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    # 'filer_addons',
    'filer_addons.filer_gui',
    'filer_addons.filer_gui.change_list',
    'filer_addons.filer_utils',
    'filer_addons.tests.testapp',
    # those
    'easy_thumbnails',
    'filer',
    'mptt',
    'polymorphic',
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


# =============================================================================
# DJANGO FILER settings
# =============================================================================


FILER_IS_PUBLIC_DEFAULT = True
FILER_ENABLE_PERMISSIONS = False
FILER_PAGINATE_BY = 200
FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True
FILER_STORAGES = {
    'public': {
        'main': {
            # 'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {},
            'UPLOAD_TO': 'filer_addons.filer_utils.generate_folder_and_filename.no_subfolders', # NOQA
            # 'UPLOAD_TO': 'filer_addons.filer_utils.generate_folder_and_filename.complete_db_folder', # NOQA
            'UPLOAD_TO_PREFIX': 'filer',
        },
        'thumbnails': {
            # 'ENGINE': 'filer.storage.PublicFileSystemStorage',
            # 'OPTIONS': {},
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'filer_thumbnails',
            },
        },
    },
}
