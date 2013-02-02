#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + os.sep)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_js_reverse.tests.'

from django.test.client import Client
from django.utils import unittest
from django.test import TestCase


class JSReverseViewTestCase(TestCase):
    urls = 'django_js_reverse.tests.test_urls'

    def test_view_no_url_args(self):
        client = Client()
        response = client.post('/jsreverse/')
        self.assertContains(response, "'test_no_url_args', ['test_no_url_args/', []]")

    def test_view_one_url_arg(self):
        client = Client()
        response = client.post('/jsreverse/')
        self.assertContains(response, "'test_one_url_args', ['test_one_url_args/%(arg_one)s/', ['arg_one']]")

    def test_view_two_url_args(self):
        client = Client()
        response = client.post('/jsreverse/')
        self.assertContains(response, "test_two_url_args', ['test_one_url_args/%(arg_one)s\u002D%(arg_two)s/', ['arg_one','arg_two']]")

if __name__ == '__main__':
    unittest.main()