# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django_js_reverse.core import generate_js

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver


register = template.Library()


@register.simple_tag(takes_context=True)
def js_reverse_inline(context):
    """
    Outputs a string of javascript that can generate URLs via the use
    of the names given to those URLs.
    """
    if 'request' in context:
        default_urlresolver = get_resolver(getattr(context['request'], 'urlconf', None))
    else:
        default_urlresolver = get_resolver(None)
    return mark_safe(generate_js(default_urlresolver))
