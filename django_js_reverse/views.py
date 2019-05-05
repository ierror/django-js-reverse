# -*- coding: utf-8 -*-
import json

from django import http
from django_js_reverse import core

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver


def _urls_js(fn, type):
    def view(request):
        default_urlresolver = get_resolver(getattr(request, 'urlconf', None))
        return http.HttpResponse(fn(default_urlresolver), content_type=type)

    return view


def _generate_json(*args, **kwargs):
    return json.dumps(core.generate_json(*args, **kwargs))


urls_js = _urls_js(core.generate_js, 'application/javascript')
urls_json = _urls_js(_generate_json, 'application/json')
