import os
import shutil

from django.utils.translation import gettext_lazy as _
from filer import settings as filer_settings

from .base import SubcommandsCommand


# TODO: use filer storage for removing!??
# TODO: also remove private files?
class DeleteThumbnailsCommand(SubcommandsCommand):
    help_string = _('Delete all generated thumbnails.')
    command_name = 'delete_thumbnails'
    storage = filer_settings.FILER_PUBLICMEDIA_STORAGE
    storage_private = filer_settings.FILER_PRIVATEMEDIA_STORAGE

    def handle(self, *args, **options):
        self._remove_thumbs(self.storage, 'public')
        self.stdout.write("Only removing public thumbnails for now. Bye.")

    def _remove_thumbs(self, storage, public_private):
        try:
            thumb_prefix = filer_settings.FILER_STORAGES[public_private]['thumbnails']['THUMBNAIL_OPTIONS']['base_dir']  # noqa
        except KeyError:
            self.stdout.write(
                "No valid settings found ({} storage)! Aborting.".format(
                    public_private))
            return
        path = os.path.join(storage.location, thumb_prefix)
        if os.path.isdir(path):
            self.stdout.write("Removing: %s" % path)
            shutil.rmtree(path)
        else:
            self.stdout.write("Not a directory: %s" % path)
