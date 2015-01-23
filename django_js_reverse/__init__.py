# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname

VERSION = (0, 4, 0)


def save_js_file():
    # placed here to past test and setup
    from django.core.files.storage import FileSystemStorage
    from django.core.files.base import ContentFile
    from . views import urls_js

    package_path = dirname(__file__)
    location = join(package_path, 'static', 'django_js_reverse', 'js')
    file = 'reverse.js'
    fs = FileSystemStorage(location=location)
    if fs.exists(file):
        fs.delete(file)

    content = urls_js()
    fs.save(file, ContentFile(content))


if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic']:  # , 'runserver'
    save_js_file()
