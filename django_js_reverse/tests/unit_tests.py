#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.test.client import Client
from django.utils import unittest
from django.test import TestCase
from django.test.utils import override_settings


class JSReverseViewTestCase(TestCase):
    client = None
    urls = 'django_js_reverse.tests.test_urls'

    def setUp(self):
        self.client = Client()

    def test_view_no_url_args(self):
        response = self.client.post('/jsreverse/')
        self.assertContains(response, "'test_no_url_args', ['test_no_url_args/', []]")

    def test_view_one_url_arg(self):
        response = self.client.post('/jsreverse/')
        self.assertContains(response, "'test_one_url_args', ['test_one_url_args/%(arg_one)s/', ['arg_one']]")

    def test_view_two_url_args(self):
        response = self.client.post('/jsreverse/')
        self.assertContains(
            response, "test_two_url_args', ['test_two_url_args/%(arg_one)s\u002D%(arg_two)s/', ['arg_one','arg_two']]")

    @override_settings(JS_REVERSE_JS_VAR_NAME='Foo')
    def test_js_var_name_changed_valid(self):
        response = self.client.post('/jsreverse/')
        self.assertContains(response, 'exports.Foo = (function () {')

    @override_settings(JS_REVERSE_JS_VAR_NAME='1test')
    def test_js_var_name_changed_invalid(self):
        from django.core.exceptions import ImproperlyConfigured
        with self.assertRaises(ImproperlyConfigured):
            self.client.post('/jsreverse/')


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + os.sep)
    unittest.main()