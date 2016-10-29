# -*- coding: utf-8 -*-
import re
import sys

from django.conf import settings
from django.core import urlresolvers
from django.conf.urls import RegexURLPattern, RegexURLResolver
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.utils.regex_helper import normalize

from . import rjsmin
from .js_reverse_settings import (JS_EXCLUDE_NAMESPACES, JS_GLOBAL_OBJECT_NAME,
                                  JS_INCLUDE_ONLY_NAMESPACES, JS_MINIFY,
                                  JS_VAR_NAME)

if sys.version < '3':
    text_type = unicode  # NOQA
else:
    text_type = str


JS_IDENTIFIER_RE = re.compile(r'^[$A-Z_][\dA-Z_$]*$')


def test_exclude(namespace, exclude_ns):
    exclude_allow = True
    for ns in exclude_ns:
        if ns != "" and namespace.startswith(ns):
            exclude_allow = False
            break
    return exclude_allow


def test_include_only(namespace, include_only_ns):
    include_only_allow = True
    if include_only_ns != []:
        # True mean that ns passed the test
        in_on_empty_ns = False
        in_on_is_in_list = False
        in_on_null = False

        # Test urls without ns
        if namespace == '' and '' in include_only_ns:
            in_on_empty_ns = True

        # check if nestead ns isn't subns of include_only ns
        # e.g. ns = "foo:bar" include_only = ["foo"] -> this ns will be used
        # works for ns = "lorem:ipsum:dolor" include_only = ["lorem:ipsum"]
        # ns "lorem" will be ignored but "lorem:ipsum" & "lorem:ipsum:.." won't
        for ns in include_only_ns:
            if ns != "" and namespace.startswith(ns):
                in_on_is_in_list = True
                break

        # Test if isn't used "\0" flag
        # use "foo\0" to add urls just from "foo" not from subns "foo:bar"
        if namespace + '\0' in include_only_ns:
            in_on_null = True

        include_only_allow = in_on_empty_ns or in_on_is_in_list or in_on_null
    return include_only_allow


def clean_patttern(pattern):
    if pattern.startswith('^'):
        pattern = pattern[1:]
    return pattern


def build_url_dict(url_resolver, exclude=[], include=[], parent_pattern="", namespace=""):
    """
    returns dict of tuples {<url_name>: <url_patern_tuple>, ...}
    """
    patterns = {}
    for up in url_resolver.url_patterns:
        if isinstance(up, RegexURLResolver):
            if up.namespace:
                next_namespace = namespace + up.namespace + ":"
            else:
                next_namespace = namespace
            next_parent_pattern = parent_pattern + clean_patttern(up.regex.pattern)
            next_patterns = build_url_dict(up, exclude, include, next_parent_pattern, next_namespace)
            patterns.update(next_patterns)
        elif isinstance(up, RegexURLPattern):
            if not up.name:
                continue
            if (not test_exclude(namespace, exclude) or
                not test_include_only(namespace, include)):
                continue
            new_pattern = parent_pattern + clean_patttern(up.regex.pattern)
            new_pattern = normalize(new_pattern)[0]
            name = namespace + up.name
            if patterns.get(name, False):
                patterns[name].append(new_pattern)
            else:
                patterns[name] = [new_pattern]
    return patterns


def prepare_url_list(urlresolver):
    """
    returns list of tuples [(<url_name>, <url_patern_tuple> ), ...]
    """
    exclude_ns = getattr(settings, 'JS_REVERSE_EXCLUDE_NAMESPACES', JS_EXCLUDE_NAMESPACES)
    include_only_ns = getattr(settings, 'JS_REVERSE_INCLUDE_ONLY_NAMESPACES', JS_INCLUDE_ONLY_NAMESPACES)

    if exclude_ns and include_only_ns:
        raise ImproperlyConfigured(
            'Neither use JS_REVERSE_EXCLUDE_NAMESPACES nor JS_REVERSE_INCLUDE_ONLY_NAMESPACES setting')

    patterns = build_url_dict(urlresolver, exclude_ns, include_only_ns)

    return ([k,v] for k, v in patterns.items())


def generate_js(default_urlresolver):
    js_var_name = getattr(settings, 'JS_REVERSE_JS_VAR_NAME', JS_VAR_NAME)
    if not JS_IDENTIFIER_RE.match(js_var_name.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (js_var_name))

    js_global_object_name = getattr(settings, 'JS_REVERSE_JS_GLOBAL_OBJECT_NAME', JS_GLOBAL_OBJECT_NAME)
    if not JS_IDENTIFIER_RE.match(js_global_object_name.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_GLOBAL_OBJECT_NAME setting "%s" is not a valid javascript identifier.' % (
                js_global_object_name))

    minfiy = getattr(settings, 'JS_REVERSE_JS_MINIFY', JS_MINIFY)
    if not isinstance(minfiy, bool):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_MINIFY setting "%s" is not a valid. Needs to be set to True or False.' % (minfiy))

    script_prefix_via_config = getattr(settings, 'JS_REVERSE_SCRIPT_PREFIX', None)
    if script_prefix_via_config:
        script_prefix = script_prefix_via_config
        if not script_prefix.endswith('/'):
            script_prefix = '{0}/'.format(script_prefix)
    else:
        script_prefix = urlresolvers.get_script_prefix()

    js_content = loader.render_to_string('django_js_reverse/urls_js.tpl', {
        'urls': sorted(list(prepare_url_list(default_urlresolver))),
        'url_prefix': script_prefix,
        'js_var_name': js_var_name,
        'js_global_object_name': js_global_object_name,
    })

    if minfiy:
        js_content = rjsmin.jsmin(js_content)
    return js_content
