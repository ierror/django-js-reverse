# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.http import HttpResponse
from django_js_reverse.core import generate_js


def urls_js(request):
    default_urlresolver = urlresolvers.get_resolver(getattr(request, 'urlconf', None))
    response_body = generate_js(default_urlresolver)
    return HttpResponse(response_body, **{'content_type': 'application/javascript'})
