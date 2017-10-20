# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil

from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import DefaultStorage
from filer.settings import FILER_STORAGES

from .base import SubcommandsCommand


class DeleteThumbnailsCommand(SubcommandsCommand):
    help_string = _('Delete all generated thumbnailss.')
    command_name = 'delete_thumbnails'
    storage = DefaultStorage()

    def handle(self, *args, **options):
        try:
            thumb_prefix = FILER_STORAGES['public']['thumbnails']['THUMBNAIL_OPTIONS']['base_dir']
        except KeyError:
            self.stdout.write("No valid settings found! Aborting.")
            return
        path = os.path.join(self.storage.location, thumb_prefix)
        self.stdout.write("Removing: %s" % path)
        shutil.rmtree(path)
