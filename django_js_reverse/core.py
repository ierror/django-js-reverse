# -*- coding: utf-8 -*-
import json
import re
import sys
from distutils.version import LooseVersion

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from . import rjsmin
from .js_reverse_settings import (JS_EXCLUDE_NAMESPACES, JS_GLOBAL_OBJECT_NAME,
                                  JS_INCLUDE_ONLY_NAMESPACES, JS_MINIFY,
                                  JS_VAR_NAME)

try:
    from django import urls as urlresolvers
except ImportError:
    from django.core import urlresolvers

if sys.version < '3':
    text_type = unicode  # NOQA
else:
    text_type = str

JS_IDENTIFIER_RE = re.compile(r'^[$A-Z_][\dA-Z_$]*$')


def prepare_url_list(urlresolver, namespace_path='', namespace=''):
    """
    returns list of tuples [(<url_name>, <url_patern_tuple> ), ...]
    """
    exclude_ns = getattr(settings, 'JS_REVERSE_EXCLUDE_NAMESPACES', JS_EXCLUDE_NAMESPACES)
    include_only_ns = getattr(settings, 'JS_REVERSE_INCLUDE_ONLY_NAMESPACES', JS_INCLUDE_ONLY_NAMESPACES)

    if exclude_ns and include_only_ns:
        raise ImproperlyConfigured(
            'Neither use JS_REVERSE_EXCLUDE_NAMESPACES nor JS_REVERSE_INCLUDE_ONLY_NAMESPACES setting')

    if namespace[:-1] in exclude_ns:
        return

    include_only_allow = True  # include_only state varible

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
            if ns != "" and namespace[:-1].startswith(ns):
                in_on_is_in_list = True
                break

        # Test if isn't used "\0" flag
        # use "foo\0" to add urls just from "foo" not from subns "foo:bar"
        if namespace[:-1] + '\0' in include_only_ns:
            in_on_null = True

        include_only_allow = in_on_empty_ns or in_on_is_in_list or in_on_null

    if include_only_allow:
        for url_name in urlresolver.reverse_dict.keys():
            if isinstance(url_name, (text_type, str)):
                url_patterns = []
                for url_pattern in urlresolver.reverse_dict.getlist(url_name):
                    url_patterns += [
                        [namespace_path + pat[0], pat[1]] for pat in url_pattern[0]]
                yield [namespace + url_name, url_patterns]

    for inner_ns, (inner_ns_path, inner_urlresolver) in \
            urlresolver.namespace_dict.items():
        inner_ns_path = namespace_path + inner_ns_path
        inner_ns = namespace + inner_ns + ':'

        # if we have inner_ns_path, reconstruct a new resolver so that we can
        # handle regex substitutions within the regex of a namespace.
        if inner_ns_path:
            args = [inner_ns_path, inner_urlresolver]

            # https://github.com/ierror/django-js-reverse/issues/65
            if LooseVersion(django.get_version()) >= LooseVersion("2.0.6"):
                args.append(tuple(urlresolver.pattern.converters.items()))

            inner_urlresolver = urlresolvers.get_ns_resolver(*args)
            inner_ns_path = ''

        for x in prepare_url_list(inner_urlresolver, inner_ns_path, inner_ns):
            yield x


def generate_json(default_urlresolver, script_prefix=None):
    if script_prefix is None:
        script_prefix = urlresolvers.get_script_prefix()

    urls = sorted(list(prepare_url_list(default_urlresolver)))

    return {
        'urls': [
            [
                force_text(name),
                [
                    [force_text(path), [force_text(arg) for arg in args]]
                    for path, args in patterns
                ],
            ] for name, patterns in urls
        ],
        'prefix': script_prefix,
    }


def _safe_json(obj):
    return mark_safe(
        json
        .dumps(obj)
        .replace('>', '\\u003E')
        .replace('<', '\\u003C')
        .replace('&', '\\u0026')
    )


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

    data = generate_json(default_urlresolver, script_prefix)
    js_content = loader.render_to_string('django_js_reverse/urls_js.tpl', {
        'data': _safe_json(data),
        'js_name': '.'.join([js_global_object_name, js_var_name]),
    })

    if minfiy:
        js_content = rjsmin.jsmin(js_content)
    return js_content
