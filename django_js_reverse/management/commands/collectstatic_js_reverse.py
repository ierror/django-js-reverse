# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname
from django.core.management.base import BaseCommand

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django_js_reverse.views import urls_js
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates a static urls-js file for django-js-reverse'

    def handle(self, *args, **options):
            location = join(settings.STATIC_ROOT, 'django_js_reverse', 'js')
            file = 'reverse.js'
            fs = FileSystemStorage(location=location)
            if fs.exists(file):
                fs.delete(file)

            content = urls_js()
            fs.save(file, ContentFile(content))
            if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_js_reverse']:
                self.stdout.write('js-reverse file written to %s' % (location))
