
from django.conf import settings


# defaults: the most greedy possible!
FILER_ADDONS_DUPLICATE_HANDLING = getattr(
    settings, 'FILER_ADDONS_DUPLICATE_HANDLING', {
        'prevent': True,
        'created_only': False,
        'same_folder_required': False,
        'same_filename_required': False,
        # TODO: as own setting/signal? 'rename_files': True,
    }
)

FILER_ADDONS_RENAME_FILES = getattr(
    settings, 'FILER_ADDONS_RENAME_FILES', True
)

FILER_ADDONS_UNFILED_HANDLING = getattr(
    settings, 'FILER_ADDONS_UNFILED_HANDLING', {
        'move_unfiled': True,
        'created_only': False,
        'default_folder_name': '0 - Direct Uploads',
    }
)
