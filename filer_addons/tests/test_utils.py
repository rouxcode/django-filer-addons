# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class FilerUtilsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='fred',
            password='test',
            email='test@test.fred',
        )

    def tearDown(self):
        pass

    def test_has_css(self):
        self.client.login(username='fred', password='test')
        url = reverse('admin:filer_folder_changelist')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
