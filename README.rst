Django JS Reverse
=================
.. image:: https://badge.fury.io/py/django-js-reverse.png
   :target: http://badge.fury.io/py/django-js-reverse

.. image:: https://travis-ci.org/ierror/django-js-reverse.png
   :target: http://travis-ci.org/ierror/django-js-reverse

.. image:: https://coveralls.io/repos/ierror/django-js-reverse/badge.png?branch=develop
   :alt: Coverage Status
   :target: https://coveralls.io/r/ierror/django-js-reverse?branch=develop

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

Changelog
_________
    0.4.1
        Fix: collectstatic runner: moved to own management command collectstatic_js_reverse
             

    0.4.0
        Add ability to save in file
        <script src="{% static 'django_js_reverse/js/reverse.js' %}"></script>
        to do this run ./manage.py collectstatic

        Add JS_REVERSE_EXCLUDE_NAMESPACES option
        to exclude namespaces from import
        default is []

        To exclude e.g. admin and Django Debug Toolbar:
        ::
            JS_REVERSE_EXCLUDE_NAMESPACES = ['admin', 'djdt']

        Thank you Andertaker

    0.3.4
        New: Support for nested namespaces. Thank you hyperair

        New: Support for arguments within namespace path. Thank you hyperair

        New: Support for optional url arguments. Thank you hyperair

    0.3.3
        New: Django 1.7 support

    0.3.2
        New: Default minification of the generated javascript file

        Fix: content type of the jsreverse script. Thank you @emcsween

        Testing: Use selenium for better testing

    0.3.1
        Added support for namespaces


    0.3.0
        Test support for pypy, python 3.4, django 1.6

        Refactored include of JS_REVERSE_JS_VAR_NAME js var name

        Get rid of "DeprecationWarning: The mimetype keyword argument is depracated, use content_type instead"

Requirements
------------

-  Python (2.6, 2.7, 3.1, 3.3, 3.4, PyPy)
-  Django (1.4, 1.5, 1.6, 1.7)

Installation
------------

Install using ``pip`` …

::

    pip install django-js-reverse

… or clone the project from github.

::

    git clone git@github.com:ierror/django-js-reverse.git

Add ``'django_js_reverse'`` to your ``INSTALLED_APPS`` setting.

::

    INSTALLED_APPS = (
        ...
        'django_js_reverse',        
    )


Usage as static file
--------------------

First generate static file by
::
    ./manage.py collectstatic_js_reverse

If you change some urls or add plagin and wont to update reverse.js file
run the command again.

After this add file to template
::
    <script src="{% static 'django_js_reverse/js/reverse.js' %}"></script>




Usage with views
----------------

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


Options
-------

Optional you can overwrite the default javascript variable ‘Urls’ used
to access the named urls by django setting

::

    JS_REVERSE_JS_VAR_NAME = 'Urls'

Optional you can disable the minfication of the generated javascript file
by django setting

::

    JS_REVERSE_JS_MINIFY = False


By default all namespaces are included
::
    JS_REVERSE_EXCLUDE_NAMESPACES = []
Add some namespaces things to exclude
::
    JS_REVERSE_EXCLUDE_NAMESPACES = ['admin', 'djdt', ...]



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
    Urls['namespace:betterliving-get-house']('house', 12)

License
-------

`MIT`_

Contact
-------

`@i_error <https://twitter.com/i_error>`_

--------------

Enjoy!

.. _named urls: https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns
.. _MIT: https://raw.github.com/ierror/django-js-reverse/develop/LICENSE
