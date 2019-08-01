#!/usr/bin/env python3
import django
from django.conf import settings

from django_js_reverse import core


def main():
    settings.configure(
        INSTALLED_APPS=["django_js_reverse"],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            }
        ],
    )
    django.setup()

    module = core.generate_cjs_module()
    with open("index.js", "w") as cjs:
        cjs.write(module)

    with open("index.mjs", "w") as cjs:
        cjs.write("const module = {};")
        cjs.write(module)
        cjs.write("export default module.exports;")


if __name__ == "__main__":
    main()
