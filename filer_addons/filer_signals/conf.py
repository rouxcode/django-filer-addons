
from django.conf import settings


# defaults: sane defaults, only new uploaded, withing same folder,
# filename doesnt matter
FILER_ADDONS_DUPLICATE_HANDLING = getattr(
    settings, 'FILER_ADDONS_DUPLICATE_HANDLING', {
        'prevent': True,
        'created_only': True,
        'same_folder_required': True,
        'same_filename_required': False,
    }
)


# yep, do it
FILER_ADDONS_RENAME_FILES = getattr(
    settings, 'FILER_ADDONS_RENAME_FILES', True
)


# also move already existing, that are modified
FILER_ADDONS_UNFILED_HANDLING = getattr(
    settings, 'FILER_ADDONS_UNFILED_HANDLING', {
        'move_unfiled': True,
        'created_only': False,
        'default_folder_name': '0 - Direct Uploads',
    }
)
