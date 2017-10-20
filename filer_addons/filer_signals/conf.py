
from django.conf import settings


# defaults: sane defaults, only new uploaded, within same folder,
# filename doesnt matter
# warning: setting created_only to False will merge all existing duplicates.
FILER_ADDONS_DUPLICATE_HANDLING = getattr(
    settings, 'FILER_ADDONS_DUPLICATE_HANDLING', {
        'prevent': True,
        'created_only': True,
        'same_folder_required': True,
        'same_filename_required': False,
    }
)
setattr(settings, 'FILER_ADDONS_DUPLICATE_HANDLING', FILER_ADDONS_DUPLICATE_HANDLING)


# yep, do it
FILER_ADDONS_RENAME_FILES = getattr(
    settings, 'FILER_ADDONS_RENAME_FILES', True
)
setattr(settings, 'FILER_ADDONS_RENAME_FILES', FILER_ADDONS_RENAME_FILES)


# also move already existing, that are modified
FILER_ADDONS_UNFILED_HANDLING = getattr(
    settings, 'FILER_ADDONS_UNFILED_HANDLING', {
        'move_unfiled': True,
        'created_only': False,
        'default_folder_name': '0 - Direct Upload',
    }
)
setattr(settings, 'FILER_ADDONS_UNFILED_HANDLING', FILER_ADDONS_UNFILED_HANDLING)
