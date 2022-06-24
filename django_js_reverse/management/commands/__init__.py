__author__ = 'boerni'

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django_js_reverse.js_reverse_settings import JS_OUTPUT_PATH

class CollectStaticCommand(BaseCommand):
    requires_system_checks = False
    def get_location(self):
        output_path = getattr(settings, 'JS_REVERSE_OUTPUT_PATH', JS_OUTPUT_PATH)
        if output_path:
            return output_path

        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            raise ImproperlyConfigured(
                'The collectstatic_js_reverse command needs settings.JS_REVERSE_OUTPUT_PATH or settings.STATIC_ROOT to be set.')

        return os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js')
