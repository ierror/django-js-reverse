# -*- coding: utf-8 -*-
from django import template
from django_js_reverse.views import urls_js


register = template.Library()


@register.simple_tag()
def js_reverse_inline():
    """
    Outputs a string of javascript that can generate URLs via the use
    of the names given to those URLs.
    """
    return urls_js()
