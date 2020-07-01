
from django.conf import settings


# defaults: sane defaults, only new uploaded, within same folder,
# filename doesnt matter
# warning: setting created_only to False will merge all existing duplicates.
FILER_ADDONS_DUPLICATE_HANDLING = getattr(
    settings,
    'FILER_ADDONS_DUPLICATE_HANDLING',
    {
        'prevent': True,
        'created_only': True,
        'same_folder_required': True,
        'same_filename_required': False,
    }
)

# yep, do it. nice when replacing files! no need for orphaned files fix!
FILER_ADDONS_CONSISTENT_FILENAMES = getattr(
    settings,
    'FILER_ADDONS_CONSISTENT_FILENAMES',
    True
)

# fix orphaned files when replacing a file
# https://github.com/divio/django-filer/pull/958
FILER_ADDONS_REPLACE_FIX = getattr(
    settings,
    'FILER_ADDONS_REPLACE_FIX',
    False
)

# also move already existing, that are modified
FILER_ADDONS_UNFILED_HANDLING = getattr(
    settings,
    'FILER_ADDONS_UNFILED_HANDLING',
    {
        'move_unfiled': True,
        'created_only': False,
        'default_folder_name': '0 - Direct Upload',
    }
)
