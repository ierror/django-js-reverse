# -*- coding: utf-8 -*-
import re
import sys

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


def urls_js(request):
    js_var_name = getattr(settings, 'JS_REVERSE_JS_VAR_NAME', JS_VAR_NAME)

    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', js_var_name.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (js_var_name))

    url_patterns = list(urlresolvers.get_resolver(None).reverse_dict.items())
    url_list = [(url_name, url_pattern[0][0]) for url_name, url_pattern in url_patterns if
                (isinstance(url_name, str) or isinstance(url_name, text_type))]

    view_kwargs = {
        'context_instance': RequestContext(request),
        content_type_keyword_name: content_type_keyword_name
    }
    return render_to_response('django_js_reverse/urls_js.tpl',
                              {
                                  'urls': url_list,
                                  'url_prefix': urlresolvers.get_script_prefix(),
                                  'js_var_name': js_var_name
                              }, **view_kwargs)
