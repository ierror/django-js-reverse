#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import json
import os
import re
import subprocess
import sys
import unittest

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.template import Context, RequestContext, Template
from django.utils.encoding import smart_str
from helper import is_django_ver_gte_2
from utils import script_prefix

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + os.sep)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.test import TestCase, RequestFactory  # noqa: E402 isort:skip
from django.test.client import Client  # noqa: E402 isort:skip
from django.test.utils import override_settings  # noqa: E402 isort:skip


class AbstractJSReverseTestCase(object):
    client = Client()

    @classmethod
    def setUpClass(cls):
        if hasattr(django, 'setup'):
            # for django >= 1.7
            django.setup()
        super(AbstractJSReverseTestCase, cls).setUpClass()

    def assertEqualJSEval(self, js, url_call, expected_url):
        script = '{}return {};'.format(js, url_call)
        module = 'console.log(new Function({})());'.format(json.dumps(script))
        stdout = (
            subprocess
            .check_output(['node', '-e', module.encode('utf8')])
            .decode('utf8')
        )
        self.assertEqual(re.sub(r'\n$', '', stdout), expected_url)

    def assertEqualJSUrlEval(self, *args, **kwargs):
        js = smart_str(self.client.post('/jsreverse/').content)
        self.assertEqualJSEval(js, *args, **kwargs)


@override_settings(ROOT_URLCONF='django_js_reverse.tests.test_urls')
class JSReverseViewTestCaseMinified(AbstractJSReverseTestCase, TestCase):
    def test_view_no_url_args(self):
        self.assertEqualJSUrlEval('Urls.test_no_url_args()', '/test_no_url_args/')

    def test_camel_case(self):
        self.assertEqualJSUrlEval('Urls.testNoUrlArgs()', '/test_no_url_args/')

    def test_view_one_url_arg(self):
        self.assertEqualJSUrlEval('Urls.test_one_url_args("arg_one")', '/test_one_url_args/arg_one/')

    def test_view_two_url_args(self):
        self.assertEqualJSUrlEval('Urls.test_two_url_args("arg_one", "arg_two")', '/test_two_url_args/arg_one-arg_two/')

    def test_view_optional_url_arg(self):
        self.assertEqualJSUrlEval('Urls.test_optional_url_arg("arg_two")',
                                  '/test_optional_url_arg/2_arg_two/')
        self.assertEqualJSUrlEval('Urls.test_optional_url_arg("arg_one", "arg_two")',
                                  '/test_optional_url_arg/1_arg_one-2_arg_two/')

    def test_unicode_url_name(self):
        self.assertEqualJSUrlEval('Urls.test_unicode_url_name()', '/test_unicode_url_name/')

    @override_settings(JS_REVERSE_JS_VAR_NAME='Foo')
    def test_js_var_name_changed_valid(self):
        self.assertEqualJSUrlEval('Foo.test_no_url_args()', '/test_no_url_args/')

    @override_settings(JS_REVERSE_JS_VAR_NAME='1test')
    def test_js_var_name_changed_to_invalid(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post('/jsreverse/')

    def test_namespaces(self):
        self.assertEqualJSUrlEval('Urls["ns1:test_two_url_args"]("arg_one", "arg_two")',
                                  '/ns1/test_two_url_args/arg_one-arg_two/')
        self.assertEqualJSUrlEval('Urls["ns2:test_two_url_args"]("arg_one", "arg_two")',
                                  '/ns2/test_two_url_args/arg_one-arg_two/')

    def test_namespaces_with_args(self):
        self.assertEqualJSUrlEval('Urls["ns_arg:test_two_url_args"]("arg_one", "arg_two", "arg_three")',
                                  '/nsarg_one/test_two_url_args/arg_two-arg_three/')

    def test_namespaces_nested(self):
        self.assertEqualJSUrlEval('Urls["nestedns:ns1:test_two_url_args"]("arg_one", "arg_two")',
                                  '/nestedns/ns1/test_two_url_args/arg_one-arg_two/')

    def test_content_type(self):
        response = self.client.post('/jsreverse/')
        self.assertEqual(response['Content-Type'], 'application/javascript')

    @override_settings(JS_REVERSE_JS_MINIFY='invalid')
    def test_js_minfiy_changed_to_invalid(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post('/jsreverse/')

    def test_namespace_in_urls(self):
        response = self.client.get('/jsreverse/')
        self.assertContains(response, 'exclude_namespace', status_code=200)

    @override_settings(JS_REVERSE_EXCLUDE_NAMESPACES=['exclude_namespace'])
    def test_namespace_not_in_response(self):
        response = self.client.get('/jsreverse/')
        self.assertNotContains(response, 'exclude_namespace', status_code=200)

    @override_settings(JS_REVERSE_INCLUDE_ONLY_NAMESPACES=['ns1'])
    def test_only_namespace_in_response(self):
        response = self.client.get('/jsreverse/')
        self.assertContains(response, 'ns1', status_code=200)
        self.assertNotContains(response, 'ns2', status_code=200)
        self.assertNotContains(response, 'ns_arg', status_code=200)
        self.assertNotContains(response, 'nesteadns', status_code=200)
        self.assertNotContains(response, 'exclude_namespace', status_code=200)
        self.assertNotContains(response, 'nsdn', status_code=200)
        self.assertNotContains(response, 'nsno', status_code=200)

    @override_settings(JS_REVERSE_INCLUDE_ONLY_NAMESPACES=['nsdn:nsdn'])
    def test_only_namespace_nestead_in_response(self):
        response = self.client.get('/jsreverse/')
        self.assertContains(response, 'nsdn:nsdn2:ns1', status_code=200)
        self.assertNotContains(response, 'nsdn:ns1', status_code=200)

    @override_settings(JS_REVERSE_INCLUDE_ONLY_NAMESPACES=[''])
    def test_only_empty_namespaces(self):
        response = self.client.get('/jsreverse/')
        self.assertEqualJSUrlEval('Urls["test_two_url_args"]("arg_one", "arg_two")',
                                  '/test_two_url_args/arg_one-arg_two/')
        self.assertNotContains(response, 'ns1', status_code=200)
        self.assertNotContains(response, 'ns2', status_code=200)

    @override_settings(JS_REVERSE_INCLUDE_ONLY_NAMESPACES=['nsno\0'])
    def test_only_namespaces_without_subnss(self):
        response = self.client.get('/jsreverse/')
        self.assertEqualJSUrlEval('Urls["nsno:test_two_url_args"]("arg_one", "arg_two")',
                                  '/nsno/ns1/test_two_url_args/arg_one-arg_two/')
        self.assertNotContains(response, 'nsno:nsdn0', status_code=200)

    def test_script_prefix_v1(self):
        with script_prefix('/foobarlala/'):
            self.assertEqualJSUrlEval('Urls["nestedns:ns1:test_two_url_args"]("arg_one", "arg_two")',
                                      '/foobarlala/nestedns/ns1/test_two_url_args/arg_one-arg_two/')

    def test_duplicate_name(self):
        self.assertEqualJSUrlEval('Urls.test_duplicate_name("arg_one")',
                                  '/test_duplicate_name/arg_one/')
        self.assertEqualJSUrlEval('Urls.test_duplicate_name("arg_one", "arg_two")',
                                  '/test_duplicate_name/arg_one-arg_two/')

    def test_duplicate_argcount(self):
        self.assertEqualJSUrlEval('Urls.test_duplicate_argcount({arg_one: "arg_one"})',
                                  '/test_duplicate_argcount/arg_one-/')
        self.assertEqualJSUrlEval('Urls.test_duplicate_argcount({arg_two: "arg_two"})',
                                  '/test_duplicate_argcount/-arg_two/')
        self.assertEqualJSUrlEval('Urls.test_duplicate_argcount({arg_one: "arg_one", arg_two: "arg_two"})',
                                  '/test_duplicate_argcount/arg_one-arg_two/')

    @override_settings(JS_REVERSE_INCLUDE_ONLY_NAMESPACES=['nsno\0'])
    @override_settings(JS_REVERSE_EXCLUDE_NAMESPACES=['exclude_namespace'])
    def test_include_exclude_configuration(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post('/jsreverse/')

    def test_int_args(self):
        self.assertEqualJSUrlEval('Urls.test_two_url_args(0, 5)', '/test_two_url_args/0-5/')
        self.assertEqualJSUrlEval('Urls.test_two_url_args("", 5)', '/test_two_url_args/-5/')

    def test_float_args(self):
        self.assertEqualJSUrlEval('Urls.test_two_url_args(0, 5.5)', '/test_two_url_args/0-5.5/')
        self.assertEqualJSUrlEval('Urls.test_two_url_args(0.00001, 5.5)', '/test_two_url_args/0.00001-5.5/')

    def test_django_path_syntax(self):
        if is_django_ver_gte_2():
            self.assertEqualJSUrlEval('Urls.test_django_gte_2_path_syntax(42, "foo")',
                                      '/test_django_gte_2_path_syntax/42/foo/')


@override_settings(JS_REVERSE_JS_MINIFY=False)
@override_settings(ROOT_URLCONF='django_js_reverse.tests.test_urls')
class JSReverseViewTestCaseNotMinified(JSReverseViewTestCaseMinified):
    def test_minification(self):
        js_not_minified = smart_str(self.client.post('/jsreverse/').content)
        with override_settings(JS_REVERSE_JS_MINIFY=True):
            js_minified = smart_str(self.client.post('/jsreverse/').content)
            self.assertTrue(len(js_minified) < len(js_not_minified))


@override_settings(ROOT_URLCONF='django_js_reverse.tests.test_urls')
class JSReverseViewTestCaseGlobalObjectName(JSReverseViewTestCaseMinified):
    def test_global_object_name_default(self):
        js_content = smart_str(self.client.post('/jsreverse/').content)
        self.assertTrue(js_content.startswith('this.'))

    @override_settings(JS_REVERSE_JS_GLOBAL_OBJECT_NAME='window')
    def test_global_object_name_change(self):
        js_content = smart_str(self.client.post('/jsreverse/').content)
        self.assertTrue(js_content.startswith('window.'))

    @override_settings(JS_REVERSE_JS_GLOBAL_OBJECT_NAME='1test')
    def test_global_object_name_change_invalid_identifier(self):
        with self.assertRaises(ImproperlyConfigured):
            self.client.post('/jsreverse/')


@override_settings(ROOT_URLCONF='django_js_reverse.tests.test_urls')
class JSReverseStaticFileSaveTest(AbstractJSReverseTestCase, TestCase):
    def test_reverse_js_file_save(self):
        call_command('collectstatic_js_reverse')

        path = os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js', 'reverse.js')
        f = io.open(path)
        content1 = f.read()

        r2 = self.client.get('/jsreverse/')
        content2 = r2.content.decode()

        self.assertEqual(len(content1), len(content2), 'Static file don\'t match http response content_1')
        self.assertEqual(content1, content2, 'Static file don\'t match http response content_2')

        # test for exception if STATIC_ROOT is not set
        with override_settings(STATIC_ROOT=None):
            with self.assertRaises(ImproperlyConfigured):
                call_command('collectstatic_js_reverse')

    def test_reverse_js_file_save_with_output_path_option(self):
        js_output_path = os.path.join(os.path.dirname(__file__), 'tmp', 'some_path')
        with override_settings(JS_REVERSE_OUTPUT_PATH=js_output_path):
            call_command('collectstatic_js_reverse')

            f = io.open(os.path.join(js_output_path, 'reverse.js'))
            content1 = f.read()

            r2 = self.client.get('/jsreverse/')
            content2 = r2.content.decode()

            self.assertEqual(len(content1), len(content2), 'Static file don\'t match http response content_1')
            self.assertEqual(content1, content2, 'Static file don\'t match http response content_2')

            # should not raise ImproperlyConfigured exception if STATIC_ROOT is not set
            with override_settings(STATIC_ROOT=None):
                call_command('collectstatic_js_reverse')

    def test_script_prefix_noslash(self):
        script_prefix = '/test/foo/bar'
        with override_settings(JS_REVERSE_SCRIPT_PREFIX=script_prefix):
            self.assertEqualJSUrlEval('Urls.test_no_url_args()', '{0}/test_no_url_args/'.format(script_prefix))

    def test_script_prefix(self):
        script_prefix = '/test/foo/bar/'
        with override_settings(JS_REVERSE_SCRIPT_PREFIX=script_prefix):
            self.assertEqualJSUrlEval('Urls.test_no_url_args()', '{0}test_no_url_args/'.format(script_prefix))


@override_settings(
    ROOT_URLCONF='django_js_reverse.tests.test_urls',

    TEMPLATE_CONTEXT_PROCESSORS=['django.core.context_processors.request'],
)
class JSReverseTemplateTagTest(AbstractJSReverseTestCase, TestCase):
    def test_tpl_tag_with_request_in_context(self):
        request = RequestFactory().post('/jsreverse/')
        request.urlconf = 'django_js_reverse.tests.test_urlconf_urls'
        tpl = Template('{% load js_reverse %}{% js_reverse_inline %}')
        js = tpl.render(RequestContext(request))
        self.assertEqualJSEval(js, 'Urls.test_changed_urlconf()', '/test_changed_urlconf/')

    def test_tpl_tag_with_dict_request_in_context(self):
        request = {'urlconf': 'django_js_reverse.tests.test_urlconf_urls'}
        tpl = Template('{% load js_reverse %}{% js_reverse_inline %}')
        js = tpl.render(Context({'request': request}))
        self.assertEqualJSEval(js, 'Urls.test_changed_urlconf()', '/test_changed_urlconf/')

    def test_tpl_tag_without_request_in_context(self):
        context_instance = Context()
        tpl = Template('{% load js_reverse %}{% js_reverse_inline %}')
        js_from_tag = tpl.render(context_instance)
        js_from_view = smart_str(self.client.post('/jsreverse/').content)
        self.assertEqual(js_from_tag, js_from_view)

    def test_tpl_tag_escape_entities(self):
        context_instance = Context()
        tpl = Template('{% load js_reverse %}{% js_reverse_inline %}')
        js = tpl.render(context_instance)
        self.assertIn(
            '\\u003C/script\\u003E\\u003Cscript\\u003Econsole.log(\\u0026amp;)'
            '\\u003C/script\\u003E\\u003C!--',
            js,
        )

if __name__ == '__main__':
    unittest.main()
