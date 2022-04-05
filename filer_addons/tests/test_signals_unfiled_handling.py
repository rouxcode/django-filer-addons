# -*- coding: utf-8 -*-
from django.test import TestCase, override_settings, modify_settings
from filer.models import File, Folder

from filer_addons.tests.utils import create_django_file, create_superuser
from filer_addons.filer_signals import conf as signals_conf

try:
    reload
except NameError:
    from importlib import reload


UNFILED_HANDLING_DISABLED = {
    'move_unfiled': False,
}


@modify_settings(INSTALLED_APPS={
    'append': 'filer_addons.filer_signals',
})
class UnfiledHandlingTests(TestCase):

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

    def test_unfiled_to_folder(self):
        """
        checks if it respects to be disabled
        :return:
        """
        file_obj = self.create_file()
        self.assertNotEquals(file_obj.folder, None)

    @override_settings(
        FILER_ADDONS_UNFILED_HANDLING=UNFILED_HANDLING_DISABLED
    )
    def test_disabled_works(self):
        """
        checks if it respects to be disabled
        :return:
        """
        reload(signals_conf)
        file_obj = self.create_file()
        self.assertEquals(file_obj.folder, None)
