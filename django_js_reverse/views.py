# -*- coding: utf-8 -*-
try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver

from django.http import HttpResponse
from django_js_reverse.core import generate_js


def urls_js(request):
    default_urlresolver = get_resolver(getattr(request, 'urlconf', None))
    response_body = generate_js(default_urlresolver)
    return HttpResponse(response_body, **{'content_type': 'application/javascript'})
