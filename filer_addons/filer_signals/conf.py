
from django.conf import settings


FILER_ADDONS_DUPLICATE_HANDLING = getattr(
    settings, 'FILER_ADDONS_DUPLICATE_HANDLING', {
        'prevent': True,
        'same_folder_required': True,
        'same_filename_required': True,
        'rename_files': True,
    }
)


FILER_ADDONS_UNFILED_HANDLING = getattr(
    settings, 'FILER_ADDONS_UNFILED_HANDLING', {
        'move_unfiled': True,
        'default_folder_name': '0 - Direct Uploads',
    }
)
