# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class SignalsTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_duplicates_basic(self):

