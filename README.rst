Django JS Reverse
=================
.. image:: https://badge.fury.io/py/django-js-reverse.png
   :target: http://badge.fury.io/py/django-js-reverse

.. image:: https://travis-ci.org/version2/django-js-reverse.png
   :target: http://travis-ci.org/version2/django-js-reverse

.. image:: https://pypip.in/d/django-js-reverse/badge.png
   :target: https://crate.io/packages/django-js-reverse?version=latest

.. image:: https://coveralls.io/repos/version2/django-js-reverse?version/badge.png?branch=development
   :alt: Coverage Status
   :target: https://coveralls.io/r/version2/django-js-reverse

.. image:: https://pypip.in/license/django-js-reverse/badge.svg
    :target: https://pypi.python.org/pypi/django-js-reverse/

**Javascript url handling for Django that doesn’t hurt.**

Overview
--------

Django JS Reverse is a small django app that makes url handling of
`named urls`_ in javascript easy and non-annoying..

For example you can retrieve a named url:

urls.py:

::

    url(r'^/betterliving/(?P<category_slug>[-\w]+)/(?P<entry_pk>\d+)/$', 'get_house', name='betterliving_get_house'),

in javascript like:

::

    Urls.betterliving_get_house('house', 12)

Result:

::

    /betterliving/house/12/

Requirements
------------

-  Python (2.6, 2.7, 3.1, 3.3, 3.4, PyPy)
-  Django (1.4, 1.5, 1.6)

Installation
------------

Install using ``pip`` …

::

    pip install django-js-reverse

… or clone the project from github.

::

    git clone git@github.com:version2/django-js-reverse.git

Add ``'django_js_reverse'`` to your ``INSTALLED_APPS`` setting.

::

    INSTALLED_APPS = (
        ...
        'django_js_reverse',        
    )

Include none-cached view …

::

    urlpatterns = patterns('',
        url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
    )

… or a cached one that delivers the urls javascript

::

    from django_js_reverse.views import urls_js
    urlpatterns = patterns('',
        url(r'^jsreverse/$', cache_page(3600)(urls_js), name='js_reverse'),
    )

Include javascript in your template

::

    <script src="{% url js_reverse %}" type="text/javascript"></script>

or, if you are using Django > 1.5

::

    <script src="{% url 'js_reverse' %}" type="text/javascript"></script>

Optional you can overwrite the default javascript variable ‘Urls’ used
to access the named urls by django setting

::

    JS_REVERSE_JS_VAR_NAME = 'Urls'

Usage
-----

If your url names are valid javascript identifiers ([$A-Z\_][-Z\_$]\*)i
you can access them by the Dot notation:

::

    Urls.betterliving_get_house('house', 12)

If the named url contains invalid identifiers use the Square bracket
notation instead:

::

    Urls['betterliving-get-house']('house', 12)

License
-------

`MIT`_

Contact
-------

`@i_error <https://twitter.com/i_error>`_

--------------

Enjoy!

.. _named urls: https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns
.. _MIT: https://raw.github.com/version2/django-js-reverse/development/LICENSE