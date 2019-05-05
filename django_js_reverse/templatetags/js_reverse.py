# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django_js_reverse.core import generate_js

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver


register = template.Library()


urlconf = template.Variable('request.urlconf')


def _get_urlconf(context):
    try:
        return context.request.urlconf
    except AttributeError:
        pass
    try:
        return urlconf.resolve(context)
    except template.VariableDoesNotExist:
        pass


@register.simple_tag(takes_context=True)
def js_reverse_inline(context):
    """
    Outputs a string of javascript that can generate URLs via the use
    of the names given to those URLs.
    """
    return mark_safe(generate_js(get_resolver(_get_urlconf(context))))
