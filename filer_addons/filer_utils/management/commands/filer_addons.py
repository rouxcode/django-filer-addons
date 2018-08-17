
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from collections import OrderedDict

import filer_addons
from filer_addons.filer_utils.management.commands.subcommands.resolve_duplicates import ResolveDuplicatesCommand
from filer_addons.filer_utils.management.commands.subcommands.stats import StatsCommand
from .subcommands.base import SubcommandsCommand
from .subcommands.delete_thumbnails import DeleteThumbnailsCommand
from .subcommands.unused_files import UnusedFilesCommand
from .subcommands.orphaned_files import OrphanedFilesCommand


class Command(SubcommandsCommand):
    command_name = 'filer_addons'
    subcommands = OrderedDict((
        ('stats', StatsCommand),
        ('unused_files', UnusedFilesCommand),
        ('orphaned_files', OrphanedFilesCommand),
        ('delete_thumbnails', DeleteThumbnailsCommand),
        ('resolve_duplicates', ResolveDuplicatesCommand),
    ))
    missing_args_message = 'one of the available sub commands must be provided'

    subcommand_dest = 'cmd'

    def get_version(self):
        return filer_addons.__version__

    def add_arguments(self, parser):
        parser.add_argument('--version', action='version', version=self.get_version())
        super(Command, self).add_arguments(parser)
