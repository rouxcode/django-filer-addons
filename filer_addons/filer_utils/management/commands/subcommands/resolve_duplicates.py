# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.utils.translation import ugettext_lazy as _

from filer.models import File
from filer.models import Image

from .base import SubcommandsCommand


class ResolveDuplicatesCommand(SubcommandsCommand):
    help_string = _('resolve duplicates (remove detected duplicates, assign original instead)')
    command_name = 'resolve_duplicates'

    def handle(self, *args, **options):
        # implement! take care!
        self.stdout.write("Not yet!")
