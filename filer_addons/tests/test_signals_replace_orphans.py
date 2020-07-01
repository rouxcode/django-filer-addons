# -*- coding: utf-8 -*-
import os, time

from django.test import TestCase, override_settings, modify_settings
from filer.tests import create_superuser
from filer.models import File, Folder

from filer_addons.tests.utils import create_django_file
from filer_addons.filer_signals import conf as signals_conf
from .test_signals_duplicates import DUPLICATE_HANDLING_DISABLED

try:
    reload
except NameError:
    from importlib import reload


@modify_settings(INSTALLED_APPS={
    'append': 'filer_addons.filer_signals',
})
class ReplaceOrphanTests(TestCase):

    def setUp(self):
        reload(signals_conf)
        self.superuser = create_superuser()
        self.client.login(username='admin', password='secret')
        self.folder = Folder.objects.create(name='test')
        self.another_folder = Folder.objects.create(name='test')

    def tearDown(self):
        self.delete_files()
        for folder in Folder.objects.all():
            folder.delete()

    def delete_files(self):
        for f in File.objects.all():
            f.delete()

    def create_file(self, duplicates=True, **kwargs):
        """
        two files
        without args: duplicates, in "unfiled files"
        kwargs different_folder: second file in self.another_folder
        kwargs different_name: second file filename = file2.jpg
        :param duplicates:
        :param kwargs:
        :return:
        """
        size = (50, 50, )
        folder = kwargs.get('folder', None)
        filename = 'file1.jpg'
        django_file1 = create_django_file(filename=filename, size=size)
        self.file = File.objects.create(
            owner=self.superuser,
            original_filename=filename,
            file=django_file1,
            folder=folder,
        )
        self.file.save()

    @override_settings(
        # FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_DISABLED,
        FILER_ADDONS_CONSISTENT_FILENAMES=False,
        FILER_ADDONS_REPLACE_FIX=True,
    )
    def test_no_orphan(self):
        reload(signals_conf)
        # create
        self.create_file(duplicates=False)
        self.assertEquals(File.objects.all().count(), 1)
        # another
        size = (50, 709, )
        another_file = create_django_file(filename='file22.jpg', size=size)
        old_file = self.file.file
        # replace
        self.file.file = another_file
        self.file.save()
        # time.sleep(20)
        self.assertEquals(os.path.isfile(old_file.path), False)
