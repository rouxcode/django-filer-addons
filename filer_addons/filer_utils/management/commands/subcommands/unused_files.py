# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.management.base import CommandError
from django.utils.encoding import force_text
from filer.models import File

from .base import SubcommandsCommand


class UnusedFilesCommand(SubcommandsCommand):
    help_string = 'Delete files that have are not used in any filer field. WARNING: Specifying' \
                  '\'+\' as related name disables reverse lookup, and will not catch up here!'
    command_name = 'unused_files'

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', dest='delete',
                            default=False, help='Delete them!')

    def handle(self, *args, **options):
        # deprecated!
        # related = File._meta.get_all_related_objects()
        # replaced by: https://docs.djangoproject.com/en/1.11/ref/models/meta/
        related = [
            f for f in File._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
               and f.auto_created and not f.concrete
        ]
        filter_kwargs = {}
        for link in related:
            filter_kwargs[link.name] = None
        unused = File.objects.filter(**filter_kwargs)
        amount = unused.count()
        for file in unused:
            self.stdout.write(force_text(file))
            if options['delete']:
                file.delete()
        self.stdout.write("-")
        self.stdout.write("%s unused files found." % str(amount))
