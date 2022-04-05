from django.test import TestCase, override_settings, modify_settings
from filer.models import File, Folder

from filer_addons.tests.utils import create_django_file, create_superuser
from filer_addons.filer_signals import conf as signals_conf

try:
    reload
except NameError:
    from importlib import reload


DUPLICATE_HANDLING_DISABLED = {
    'prevent': False,
}

DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES = {
    'prevent': True,
    'created_only': True,
    'same_folder_required': False,
    'same_filename_required': False,
}

DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES_WITH_EXISTING = {
    'prevent': True,
    'created_only': False,
    'same_folder_required': False,
    'same_filename_required': False,
}


@modify_settings(INSTALLED_APPS={
    'append': 'filer_addons.filer_signals',
})
class DuplicatesTests(TestCase):

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

    def create_two_files(self, duplicates=True, **kwargs):
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
        size2 = (20, 20, )
        if duplicates:
            size2 = size
        folder = kwargs.get('folder', None)
        if kwargs.get('different_folder', None):
            folder2 = self.another_folder
        else:
            folder2 = folder
        filename = 'file1.jpg'
        if kwargs.get('different_name', None):
            filename2 = 'file2.jpg'
        else:
            filename2 = filename
        django_file1 = create_django_file(filename=filename, size=size)
        django_file2 = create_django_file(filename=filename2, size=size2)
        file_obj = File.objects.create(
            owner=self.superuser,
            original_filename=filename,
            file=django_file1,
            folder=folder,
        )
        file_obj.save()
        file_obj2 = File.objects.create(
            owner=self.superuser,
            original_filename=filename2,
            file=django_file2,
            folder=folder2,
        )
        file_obj2.save()

    def test_no_duplicates(self):
        # first, no duplicates
        self.create_two_files(duplicates=False)
        self.assertEquals(File.objects.all().count(), 2)
        # now, there are duplicates!
        self.create_two_files(duplicates=False)
        self.assertEquals(File.objects.all().count(), 2)

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
        reload(signals_conf)
        self.create_two_files(duplicates=True, )
        self.assertEquals(File.objects.all().count(), 2)
        # same again, dups!
        self.create_two_files(duplicates=True, )
        self.assertEquals(File.objects.all().count(), 4)

    @override_settings(
        FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES
    )
    def test_duplicates_anywhere(self):
        reload(signals_conf)
        self.create_two_files(
            duplicates=True,
            different_name=True,
            different_folder=True,
        )
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
        reload(signals_conf)
        self.create_two_files(duplicates=True, different_name=True)
        self.assertEquals(File.objects.all().count(), 2)
        with self.settings(
            FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES_WITH_EXISTING  # noqa
        ):
            reload(signals_conf)
            self.create_two_files(duplicates=True, different_name=True)
            self.assertEquals(File.objects.all().count(), 1)

    @override_settings(
        FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_DISABLED
    )
    def test_duplicates_is_not_greedy(self):
        """
        test that normal mode is not greedy
        already existing duplicates will not be merged
        :return:
        """
        reload(signals_conf)
        self.create_two_files(duplicates=True, different_name=True)
        self.assertEquals(File.objects.all().count(), 2)
        with self.settings(
                FILER_ADDONS_DUPLICATE_HANDLING=DUPLICATE_HANDLING_ALL_FOLDERS_ALL_FILES  # noqa
        ):
            reload(signals_conf)
            self.create_two_files(duplicates=True, different_name=True)
            self.assertEquals(File.objects.all().count(), 2)
