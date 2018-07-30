import os
import re

from django.core.management.base import BaseCommand
from filer.models import File, Image, Folder


def is_image(filename):
    name, ext = os.path.splitext(filename)
    if ext.lower()[1:] in ['jpg', 'jpeg', 'gif', 'png', 'tif', 'tiff']:
        return True


exclude_pattern = r'(_fb_thumb\.)|(_fancybox_thumb\.)|(_home_image\.)|(_left_col_small\.)' \
                      r'|(_partner\.)|(_people\.)|(_small\.)|(_thumbnail\.)'


class Command(BaseCommand):
    help = "Import existing files not currently in filer db, but on filesystem."

    def handle(self, *args, **options):
        from filer import settings as filer_settings
        self.storage_public = filer_settings.FILER_PUBLICMEDIA_STORAGE
        self.prefix_public = filer_settings.FILER_STORAGES['public']['main']['UPLOAD_TO_PREFIX']

        def walk(absdir, reldir, db_folder):
            storage = self.storage_public
            child_dirs, files = storage.listdir(absdir)
            for filename in files:
                matches = re.findall(exclude_pattern, filename)
                if not len(matches):
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
