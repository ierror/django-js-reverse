#!/usr/bin/env python3
import json
import os

import django
from django.conf import settings

import django_js_reverse
from django_js_reverse import core

if __name__ == '__main__':
    settings.configure(
        INSTALLED_APPS = ['django_js_reverse'],
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
    )
    django.setup()

    module = core.generate_cjs_module()
    with open('index.js', 'w') as cjs:
        cjs.write(module)

    with open('index.mjs', 'w') as cjs:
        cjs.write('const module = {};')
        cjs.write(module)
        cjs.write('export default module.exports;')

    with open('package.json', 'r+') as f:
        data = json.load(f)
        f.seek(0)
        data['version'] = '.'.join([str(v) for v in django_js_reverse.VERSION])
        json.dump(data, f, sort_keys=True, indent=2)
        f.write('\n');
        f.truncate()
