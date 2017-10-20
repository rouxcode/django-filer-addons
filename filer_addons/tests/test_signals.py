# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from filer.tests import create_image


class SignalsTests(TestCase):
    def setUp(self):
        self.img1 = create_image(size=(400, 400,))
        self.img2 = create_image(size=(600, 600,))

    def tearDown(self):
        pass

    def test_duplicates_basic(self):
        filename = filename or 'test_image.jpg'
        file_obj = django.core.files.File(open(self.filename, 'rb'), name=filename)
        image_obj = Image.objects.create(owner=self.superuser, original_filename=self.image_name, file=file_obj,
                                         folder=folder)
        image_obj.save()