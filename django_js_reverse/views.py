# -*- coding: utf-8 -*-
import re
import sys
from itertools import chain
from django.http import HttpResponse

if sys.version < '3':
    text_type = unicode
else:
    text_type = str

from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.core import urlresolvers
from django.conf import settings
from django import get_version

from slimit import minify
from .js_reverse_settings import JS_VAR_NAME, JS_MINIFY, JS_EXCLUDE_NAMESPACES


content_type_keyword_name = 'content_type'
if get_version() < '1.5':
    content_type_keyword_name = 'mimetype'


def urls_js(request=None):
    js_var_name = getattr(settings, 'JS_REVERSE_JS_VAR_NAME', JS_VAR_NAME)
    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', js_var_name.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (js_var_name))

    minfiy = getattr(settings, 'JS_REVERSE_JS_MINIFY', JS_MINIFY)
    if not isinstance(minfiy, bool):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_MINIFY setting "%s" is not a valid. Needs to be set to True or False.' % (minfiy))

    default_urlresolver = urlresolvers.get_resolver(getattr(request, 'urlconf', None))
    response_body = loader.render_to_string('django_js_reverse/urls_js.tpl', {
        'urls': list(prepare_url_list(default_urlresolver)),
        'url_prefix': urlresolvers.get_script_prefix(),
        'js_var_name': js_var_name
    })

    if minfiy:
        response_body = minify(response_body, mangle=True, mangle_toplevel=False)

    if not request:
        return response_body
    else:
        return HttpResponse(response_body, **{content_type_keyword_name: 'application/javascript'})


def prepare_url_list(urlresolver, namespace_path='', namespace=''):
    """
    returns list of tuples [(<url_name>, <url_patern_tuple> ), ...]
    """
    exclude_ns = getattr(settings, 'JS_REVERSE_EXCLUDE_NAMESPACES', JS_EXCLUDE_NAMESPACES)

    for url_name, url_pattern in urlresolver.reverse_dict.items():
        if isinstance(url_name, (text_type, str)):
            if namespace[:-1] in exclude_ns:
                continue
            yield [
                namespace + url_name,
                [[namespace_path + pat[0], pat[1]] for pat in url_pattern[0]]
            ]

    for inner_ns, (inner_ns_path, inner_urlresolver) in \
            urlresolver.namespace_dict.items():
        if namespace[:-1] in exclude_ns:
            continue
        inner_ns_path = namespace_path + inner_ns_path
        inner_ns = namespace + inner_ns + ':'

        # if we have inner_ns_path, reconstruct a new resolver so that we can
        # handle regex substitutions within the regex of a namespace.
        if inner_ns_path:
            inner_urlresolver = urlresolvers.get_ns_resolver(inner_ns_path,
                                                             inner_urlresolver)
            inner_ns_path = ''

        for x in prepare_url_list(inner_urlresolver, inner_ns_path, inner_ns):
            yield x
