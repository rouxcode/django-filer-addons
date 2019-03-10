import os
import re

from filer.models import File, Image, Folder
from filer_addons.filer_utils.management.commands.subcommands.base import SubcommandsCommand


def is_image(filename):
    name, ext = os.path.splitext(filename)
    if ext.lower()[1:] in ['jpg', 'jpeg', 'gif', 'png', 'tif', 'tiff']:
        return True


# TODO: via setting
file_exclude_pattern = r'(_fb_thumb\.)|(_fancybox_thumb\.)|(_home_image\.)|(_left_col_small\.)' \
                      r'|(_partner\.)|(_people\.)|(_small\.)|(_thumbnail\.)'
file_exclude_pattern = None


class ImportExistingFilesCommand(SubcommandsCommand):
    help_string = "Import existing files not currently in filer db, but on " \
           "filesystem. Must use --force, if you have existing files" \
           "in your database"
    command_name = 'import_existing_files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force import, with existing content in database.',
        )

    def handle(self, *args, **options):
        print("what")
        print(File.objects.count())
        if not options.get('force', False) and File.objects.count():
            raise Exception('Must use --force, you have existing files in db!')

        from filer import settings as filer_settings
        self.storage_public = filer_settings.FILER_PUBLICMEDIA_STORAGE
        self.prefix_public = filer_settings.FILER_STORAGES['public']['main']['UPLOAD_TO_PREFIX']

        def walk(absdir, reldir, db_folder):
            print("walk %s" % db_folder)
            storage = self.storage_public
            child_dirs, files = storage.listdir(absdir)
            for filename in files:
                matches = []
                if file_exclude_pattern:
                    matches = re.findall(file_exclude_pattern, filename)
                if not len(matches):
                    print(filename)
                    filename_with_relpath = os.path.join(reldir, filename)
                    # media_root = os.path.join(self.storage_public.location)
                    # filename_with_abspath = os.path.join(media_root, filename_with_relpath)
                    # django_file = DjangoFile(open(filename_with_abspath, 'rb'), name=filename)
                    file_cls = File
                    if is_image(filename):
                        file_cls = Image
                    file_cls.objects.create(
                        original_filename=filename,
                        folder=db_folder,
                        file=filename_with_relpath,
                        is_public=True,
                    )
            for child in child_dirs:
                kwargs = {}
                if db_folder:
                    kwargs['parent'] = db_folder
                new_folder, created = Folder.objects.get_or_create(name=child, **kwargs)
                walk(os.path.join(absdir, child), os.path.join(reldir, child), new_folder)

        public_path = os.path.join(self.storage_public.location, self.prefix_public)
        walk(public_path, self.prefix_public, None)
