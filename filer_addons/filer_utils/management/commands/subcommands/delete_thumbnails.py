# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# from django.core.files.storage import DefaultStorage
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
        try:
            thumb_prefix = filer_settings.FILER_STORAGES['public']['thumbnails']['THUMBNAIL_OPTIONS']['base_dir']
        except KeyError:
            self.stdout.write("No valid settings found! Aborting.")
            return
        path = os.path.join(self.storage.location, thumb_prefix)
        if os.path.isdir(path):
            self.stdout.write("Removing: %s" % path)
            shutil.rmtree(path)
        else:
            self.stdout.write("Not a directory, exiting: %s" % path)
