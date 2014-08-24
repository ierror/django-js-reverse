# -*- coding: utf-8 -*-
import re
import sys
from itertools import chain

if sys.version < '3':
    text_type = unicode
else:
    text_type = str

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.conf import settings
from django import get_version

from .settings import JS_VAR_NAME

content_type_keyword_name = 'content_type'
if get_version() < '1.5':
    content_type_keyword_name = 'mimetype'


def prepare_url_list(urlresolver, namespace_path='', namespace=''):
    """
    returns list of tuples [(<url_name>, <namespace_path>, <url_patern_tuple> ), ...]
    """
    prepared_list = []
    for url_name, url_pattern in urlresolver.reverse_dict.items():
        if isinstance(url_name, text_type) or isinstance(url_name, str):
            prepared_list.append([namespace + url_name, namespace_path, url_pattern[0][0]])
    return prepared_list


def urls_js(request):
    js_var_name = getattr(settings, 'JS_REVERSE_JS_VAR_NAME', JS_VAR_NAME)

    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', js_var_name.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (js_var_name))

    default_urlresolver = urlresolvers.get_resolver(None)

    # prepare data for namespeced urls
    named_urlresolves = [
        (n_urlresolver, namespace_path, namespace + ':')
        for namespace, (namespace_path, n_urlresolver) in default_urlresolver.namespace_dict.items()
    ]
    url_lists = [prepare_url_list(*args) for args in named_urlresolves]

    # add urls without namespaces
    url_lists.append((prepare_url_list(default_urlresolver)))

    view_kwargs = {
        'context_instance': RequestContext(request),
        content_type_keyword_name: content_type_keyword_name
    }

    return render_to_response('django_js_reverse/urls_js.tpl',
                              {
                                  'urls': chain(*url_lists),
                                  'url_prefix': urlresolvers.get_script_prefix(),
                                  'js_var_name': js_var_name
                              }, **view_kwargs)
