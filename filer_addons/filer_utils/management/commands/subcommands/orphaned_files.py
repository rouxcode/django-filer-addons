# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import DefaultStorage
from filer.settings import FILER_STORAGES

from .base import SubcommandsCommand


class OrphanedFilesCommand(SubcommandsCommand):
    """
    inspired and partly copied from:
    https://github.com/divio/django-filer/pull/912
    """
    help_string = _('List files that have no representation in the database. Public only for now')
    command_name = 'orphaned_files'
    storage = DefaultStorage()
    prefix = FILER_STORAGES['public']['main']['UPLOAD_TO_PREFIX']

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', dest='delete',
                            default=False, help='Delete them!')

    def handle(self, *args, **options):
        from filer.models.filemodels import File
        def walk(absdir, reldir):
            child_dirs, files = self.storage.listdir(absdir)
            for filename in files:
                relfilename = os.path.join(reldir, filename)
                try:
                    File.objects.get(file=relfilename)
                    # self.stdout.write("existing: %s" % relfilename)
                except File.DoesNotExist:
                    absfilename = os.path.join(absdir, filename)
                    if options['delete']:
                        self.storage.delete(absfilename)
                    self.stdout.write(absfilename)

            for child in child_dirs:
                walk(os.path.join(absdir, child), os.path.join(reldir, child))

        walk(os.path.join(self.storage.location, self.prefix), self.prefix)
