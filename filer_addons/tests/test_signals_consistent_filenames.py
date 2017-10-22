# -*- coding: utf-8 -*-
from django.test import TestCase, override_settings
from filer.tests import create_superuser
from filer.models import File, Folder

from filer_addons.tests.utils import create_django_file


class ConsistentFilenamesTests(TestCase):
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
        size = (50, 50, )
        if kwargs.get('size', None):
            size = kwargs['size']
        django_file = create_django_file(filename=filename, size=size)
        file_obj = File.objects.create(
            owner=self.superuser,
            original_filename=filename,
            file=django_file,
        )
        file_obj.save()
        return file_obj

    def test_has_correct_filename(self):
        """
        basics. if this breaks, filer has gone nuts completely!
        :return:
        """
        file_obj = self.create_file()
        file_path_name = file_obj.file.name
        # self.assertTrue(file_obj.file.name
        # self.assertEquals(file_obj.file, 2)

    def test_has_correct_name_after_update(self):
        """
        same filename, same (none) folder
        :return:
        """
        file_obj = self.create_file()
        new_django_file = create_django_file(filename='file_different_name.jpg')
        file_obj.file = new_django_file
        file_obj.save()
        print file_obj.file.name
        # self.assertEquals(File.objects.all().count(), 1)


