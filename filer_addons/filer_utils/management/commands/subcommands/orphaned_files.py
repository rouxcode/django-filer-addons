import os

from django.utils.translation import gettext_lazy as _
from filer import settings as filer_settings

from .base import SubcommandsCommand


class OrphanedFilesCommand(SubcommandsCommand):
    """
    inspired and partly copied from:
    https://github.com/divio/django-filer/pull/912
    """
    help_string = _('List files that have no representation in the database.')
    command_name = 'orphaned_files'
    storage_public = filer_settings.FILER_PUBLICMEDIA_STORAGE
    storage_private = filer_settings.FILER_PRIVATEMEDIA_STORAGE
    prefix_public = filer_settings.FILER_STORAGES['public']['main'][
        'UPLOAD_TO_PREFIX']
    prefix_private = filer_settings.FILER_STORAGES['private']['main'][
        'UPLOAD_TO_PREFIX']

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true', dest='delete',
                            default=False, help='Delete them!')

    def handle(self, *args, **options):
        from filer.models.filemodels import File

        def walk(absdir, reldir, public=True):
            storage = self.storage_public if public else self.storage_private
            child_dirs, files = storage.listdir(absdir)
            for filename in files:
                relfilename = os.path.join(reldir, filename)
                try:
                    File.objects.get(file=relfilename, is_public=public)
                except File.DoesNotExist:
                    absfilename = os.path.join(absdir, filename)
                    if options['delete']:
                        storage.delete(absfilename)
                    self.stdout.write(absfilename)
                except File.MultipleObjectsReturned:
                    pass
            for child in child_dirs:
                walk(os.path.join(absdir, child), os.path.join(reldir, child),
                     public=public)

        public_path = os.path.join(self.storage_public.location,
                                   self.prefix_public)
        walk(public_path, self.prefix_public, public=True)
        private_path = os.path.join(self.storage_private.location,
                                    self.prefix_private)
        if os.path.isdir(private_path):
            walk(private_path, self.prefix_private, public=False)
