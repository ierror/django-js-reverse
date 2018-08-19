import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

SECRET_KEY = 'wtf'

ROOT_URLCONF = None

USE_TZ = True

INSTALLED_APPS = (
    'django_js_reverse',
)

ALLOWED_HOSTS = ['testserver']

MIDDLEWARE_CLASSES = ()

MIDDLEWARE = ()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'tmp', 'static_root')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
    ('ua', 'Ukrainian'),
)
USE_I18N = True
