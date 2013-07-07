# -*- coding: utf-8 -*-
from django.conf import settings

JS_VAR_NAME = getattr(settings, 'JS_REVERSE_JS_VAR_NAME', 'Urls')

JS_AVAILABLE_NAMESPACES = getattr(settings, 'JS_REVERSE_AVAILABLE_NAMESPACES', [])