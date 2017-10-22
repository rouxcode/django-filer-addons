# -*- coding: utf-8 -*-
from django.test import TestCase, override_settings
from filer.tests import create_superuser
from filer.models import File, Folder

from filer_addons.tests.utils import create_django_file


class DuplicatesTests(TestCase):
    def setUp(self):
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

    def create_file(self, **kwargs):
        """
        two files
        kwargs size: tuple, img dimension
        kwargs name: filename
        :param kwargs:
        :return:
        """
        filename = 'file.jpg'
        if kwargs.get('name', None):
            filename = kwargs['name']
        folder = None
        if kwargs.get('folder', None):
            folder = kwargs['folder']
        size = (50, 50, )
        if kwargs.get('size', None):
            size = kwargs['size']
        django_file = create_django_file(filename=filename, size=size)
        file_obj = File.objects.create(
            owner=self.superuser,
            original_filename=filename,
            file=django_file,
            folder=folder,
        )
        file_obj.save()
        return file_obj

    def test_normal_folder_works(self):
        # first, no duplicates
        file_obj = self.create_file(folder=self.folder)
        self.assertEquals(file_obj.folder, self.folder)

    def test_has_duplicate_no_folder(self):
        """
        same filename, same (none) folder
        :return:
        """
        self.create_two_files(duplicates=True)
        self.assertEquals(File.objects.all().count(), 1)
        # same again, dups!
        self.create_two_files(duplicates=True)
        self.assertEquals(File.objects.all().count(), 1)

    def test_no_duplicate_different_folder(self):
        """
        same filename, different folder => no duplicate with default settings!
        :return:
        """
        self.create_two_files(duplicates=True, different_folder=True)
        self.assertEquals(File.objects.all().count(), 2)
        # same again, dups!
        self.create_two_files(duplicates=True, different_folder=True)
        self.assertEquals(File.objects.all().count(), 2)

    def test_duplicate_different_filename(self):
        """
        same filename, same folder => duplicate with default settings!
        :return:
        """
        self.create_two_files(duplicates=True, different_name=True)
        self.assertEquals(File.objects.all().count(), 1)
        # same again, dups!
        self.create_two_files(duplicates=True, different_name=True)
        self.assertEquals(File.objects.all().count(), 1)

    @override_settings(
        FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_DISABLED
    )
    def test_duplicate_detection_disabled(self):
        self.create_two_files(duplicates=True, )
        self.assertEquals(File.objects.all().count(), 2)
        # same again, dups!
        self.create_two_files(duplicates=True, )
        self.assertEquals(File.objects.all().count(), 4)

    @override_settings(
        FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES
    )
    def test_duplicates_anywhere(self):
        self.create_two_files(duplicates=True, different_name=True, different_folder=True)
        self.assertEquals(File.objects.all().count(), 1)
        # same again, still dups!
        self.create_two_files(
            duplicates=True,
            folder=self.folder,
            different_name=True,
            different_folder=True,
        )
        self.assertEquals(File.objects.all().count(), 1)

    @override_settings(
        FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_DISABLED
    )
    def test_duplicates_greedy(self):
        """
        test greedy mode: already existing duplicates will also be merged
        :return:
        """
        self.create_two_files(duplicates=True, different_name=True)
        self.assertEquals(File.objects.all().count(), 2)
        with self.settings(
            FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES_WITH_EXISTING
        ):
            self.create_two_files(duplicates=True, different_name=True)
            self.assertEquals(File.objects.all().count(), 1)

    @override_settings(
        FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_DISABLED
    )
    def test_duplicates_is_not_greedy(self):
        """
        test that normal mode is not greedy: already existing duplicates will not be merged
        :return:
        """
        self.create_two_files(duplicates=True, different_name=True)
        self.assertEquals(File.objects.all().count(), 2)
        with self.settings(
                FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES
        ):
            self.create_two_files(duplicates=True, different_name=True)
            self.assertEquals(File.objects.all().count(), 2)
