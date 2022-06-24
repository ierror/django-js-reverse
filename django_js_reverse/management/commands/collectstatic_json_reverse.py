# -*- coding: utf-8 -*-
import sys
import json

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django_js_reverse.core import generate_json
from django_js_reverse.management.commands import CollectStaticCommand

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver


class Command(CollectStaticCommand):
    help = 'Creates a static urls-json file for django-js-reverse'
    requires_system_checks = False

    def handle(self, *args, **options):
        location = self.get_location()
        file = 'reverse.json'
        fs = FileSystemStorage(location=location)
        if fs.exists(file):
            fs.delete(file)

        urlconf = getattr(settings, 'ROOT_URLCONF', None)
        default_urlresolver = get_resolver(urlconf)
        content = json.dumps(generate_json(default_urlresolver))
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_json_reverse']:
            self.stdout.write('%s file written to %s' % (file, location))  # pragma: no cover
