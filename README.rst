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
    0.4.5
        Fix: If you run your application under a subpath, the collectstatic_js_reverse needs to take care of this.
             You can now define a setting JS_REVERSE_SCRIPT_PREFIX that handles this issue.
             Thank you lizter for reporting the issue

    0.4.4
        Improvement: management command collectstatic_js_reverse throws an error if settings.STATIC_ROOT is not set

        Tests: exluded a debug print from test coverage

        Removed: support for django 1.4

        New: Templatetag to include js-reverse-js inline in your templates
        Thank you logston


`Full changelog  <https://raw.githubusercontent.com/ierror/django-js-reverse/production/CHANGELOG>`_


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

If you change some urls or add an app and want to update the reverse.js file,
run the command again.

After this add the file to your template
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


Usage as template tag
_____________________

    {% load js_reverse %}

    <script type="text/javascript" charset="utf-8">
        {% js_reverse_inline %}
    </script>


Use the urls in javascript
--------------------------

If your url names are valid javascript identifiers ([$A-Z\_][-Z\_$]\*)i
you can access them by the Dot notation:

::

    Urls.betterliving_get_house('house', 12)

If the named url contains invalid identifiers use the Square bracket
notation instead:

::

    Urls['betterliving-get-house']('house', 12)
    Urls['namespace:betterliving-get-house']('house', 12)


Options
-------

Optionally, you can overwrite the default javascript variable ‘Urls’ used
to access the named urls by django setting

::

    JS_REVERSE_JS_VAR_NAME = 'Urls'

Optionally, you can disable the minfication of the generated javascript file
by django setting

::

    JS_REVERSE_JS_MINIFY = False

By default all namespaces are included

::

    JS_REVERSE_EXCLUDE_NAMESPACES = []

To exclude any namespaces from the generated javascript file, add them to the `JS_REVERSE_EXCLUDE_NAMESPACES` setting

::

    JS_REVERSE_EXCLUDE_NAMESPACES = ['admin', 'djdt', ...]

If you run your application under a subpath, the collectstatic_js_reverse needs to take care of this.
Define the prefix in your django settings:
::
   JS_REVERSE_SCRIPT_PREFIX = '/myprefix/'


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
