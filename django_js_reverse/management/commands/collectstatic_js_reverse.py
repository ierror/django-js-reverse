# -*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

from django_js_reverse.views import urls_js


class Command(BaseCommand):
    help = 'Creates a static urls-js file for django-js-reverse'

    def handle(self, *args, **options):
        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            raise ImproperlyConfigured('The collectstatic_js_reverse command needs settings.STATIC_ROOT to be set.')
        location = os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js')
        file = 'reverse.js'
        fs = FileSystemStorage(location=location)
        if fs.exists(file):
            fs.delete(file)

        content = urls_js()
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_js_reverse']:
            self.stdout.write('js-reverse file written to %s' % (location))  # pragma: no cover
