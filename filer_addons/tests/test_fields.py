# -*- coding: utf-8 -*-
import django
from django.contrib.auth.models import User
from django.test import TestCase, Client

# compat thing!
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


class FilerFieldsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='fred',
            password='test',
            email='test@test.fred',
        )

    def tearDown(self):
        pass

    def test_basic(self):
        self.client.login(username='fred', password='test')
        url = reverse('admin:filer_folder_changelist')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
