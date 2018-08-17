# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import subprocess

from django.utils.translation import ugettext_lazy as _

from filer.models import File, Image, Folder

from .base import SubcommandsCommand


# TODO: use filer storage for removing!??
# TODO: also remove private files?
class StatsCommand(SubcommandsCommand):
    help_string = _('Show some useful information about filer database')
    command_name = 'stats'

    def handle(self, *args, **options):
        # basics
        files_count = File.objects.all().count()
        images_count = Image.objects.all().count()
        files_only = files_count - images_count
        self.stdout.write("Folders count: %s" % Folder.objects.all().count())
        self.stdout.write("Files count: %s" % files_only)
        self.stdout.write("Images count: % s" % images_count)
        self.stdout.write("Files + images count: %s" % files_count)
        # duplicates
        self.stdout.write("Computing duplicates...pls wait...")
        duplicates = []
        for file in File.objects.all():
            if not file.id in duplicates:
                if file.duplicates:
                    for dup in file.duplicates:
                        duplicates.append(file.id)
        self.stdout.write("Duplicates: %s" % len(duplicates))
