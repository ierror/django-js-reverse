# -*- coding: utf-8 -*-
VERSION = (0, 4, 1)

import sys
from os.path import join, dirname

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from . views import urls_js



def save_js_file():
    package_path = dirname(__file__)
    location = join(package_path, 'static', 'django_js_reverse', 'js')
    file = 'reverse.js'
    fs = FileSystemStorage(location=location)
    if fs.exists(file):
        fs.delete(file)

    content = urls_js()
    file = fs.save(file, ContentFile(content))


if sys.argv[1] in ['collectstatic']: # , 'runserver'
    save_js_file()
