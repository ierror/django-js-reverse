# -*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django_js_reverse.core import generate_js
from django_js_reverse.js_reverse_settings import JS_OUTPUT_PATH

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver


class Command(BaseCommand):
    help = 'Creates a static urls-js file for django-js-reverse'

    def get_location(self):
        output_path = getattr(settings, 'JS_REVERSE_OUTPUT_PATH', JS_OUTPUT_PATH)
        if output_path:
            return output_path

        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            raise ImproperlyConfigured(
                'The collectstatic_js_reverse command needs settings.JS_REVERSE_OUTPUT_PATH or settings.STATIC_ROOT to be set.')

        return os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js')

    def handle(self, *args, **options):
        location = self.get_location()
        file = 'reverse.js'
        fs = FileSystemStorage(location=location)
        if fs.exists(file):
            fs.delete(file)

        urlconf = getattr(settings, 'ROOT_URLCONF', None)
        default_urlresolver = get_resolver(urlconf)
        content = generate_js(default_urlresolver)
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_js_reverse']:
            self.stdout.write('js-reverse file written to %s' % (location))  # pragma: no cover
