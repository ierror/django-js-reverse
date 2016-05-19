=================
Django JS Reverse
=================

.. image:: https://img.shields.io/pypi/v/django-js-reverse.svg
   :target: https://pypi.python.org/pypi/django-js-reverse/

.. image:: https://img.shields.io/travis/ierror/django-js-reverse/production.svg
   :target: https://travis-ci.org/ierror/django-js-reverse

.. image:: https://img.shields.io/coveralls/ierror/django-js-reverse/production.svg
   :alt: Coverage Status
   :target: https://coveralls.io/r/ierror/django-js-reverse?branch=production

.. image:: https://img.shields.io/github/license/ierror/django-js-reverse.svg
    :target: https://raw.githubusercontent.com/ierror/django-js-reverse/develop/LICENSE

.. image:: https://img.shields.io/pypi/dm/django-js-reverse.svg

.. image:: https://img.shields.io/pypi/wheel/django-js-reverse.svg


**Javascript url handling for Django that doesn’t hurt.**


Overview
--------

Django JS Reverse is a small django app that makes url handling of
`named urls <https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns>`_ in javascript easy and non-annoying..

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
0.7.2
    Fix: `#42 <https://github.com/ierror/django-js-reverse/issues/42>`_ - "Templatetag js_reverse_inline breaks on Django 1.9"
    Thank you `tommikaikkonen <https://github.com/tommikaikkonen>`_

    Optimized imports

0.7.1
    Fix: `#41 <https://github.com/ierror/django-js-reverse/issues/41>`_ - make it possible to use number 0 as url argument

0.7.0
    New: By default collectstatic_js_reverse writes its output (reverse.js) to your project's STATIC_ROOT. Now You can change settings: JS_REVERSE_OUTPUT_PATH

    Thank you `mjnaderi <https://github.com/ierror/django-js-reverse/pull/36>`_

    New: Support for Django 1.9

    Thank you `mjnaderi <https://github.com/ierror/django-js-reverse/pull/37>`_

    New: It's now possible to include specific namespaces only. See JS_REVERSE_INCLUDE_ONLY_NAMESPACES setting for details.

    Thank you BrnoPCmaniak


`Full changelog <https://raw.githubusercontent.com/ierror/django-js-reverse/production/CHANGELOG>`_


Requirements
------------

-  Python (2.6, 2.7, 3.1, 3.3, 3.4, 3.5)
-  Django (1.5, 1.6, 1.7, 1.8, 1.9)


Installation
------------

Install using ``pip`` …

::

    pip install django-js-reverse

… or clone the project from github.

::

    git clone https://github.com/ierror/django-js-reverse.git

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

Optionally, you can change the name of the global object the javascript variable
used to access the named urls is attached to. Default is :code:`this`

::

    JS_REVERSE_JS_GLOBAL_OBJECT_NAME = False


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

If you want to include only specific namespaces add them to the `JS_REVERSE_INCLUDE_ONLY_NAMESPACES` setting
tips:
 * Use "" for urls without namespace
 * Use "foo\0" to include urls just from "foo" namaspace and not from any subnamespaces (e.g. "foo:bar")

::

    JS_REVERSE_INCLUDE_ONLY_NAMESPACES = ['poll', 'calendar', ...]

If you run your application under a subpath, the collectstatic_js_reverse needs to take care of this.
Define the prefix in your django settings:
::
   JS_REVERSE_SCRIPT_PREFIX = '/myprefix/'

By default collectstatic_js_reverse writes its output (reverse.js) to your project's STATIC_ROOT.
You can change the output path:

::

    JS_REVERSE_OUTPUT_PATH = 'some_path'


Running the test suite
----------------------

::

    make test

License
-------

`MIT <https://raw.github.com/ierror/django-js-reverse/develop/LICENSE>`_


Contact
-------

`@i_error <https://twitter.com/i_error>`_

--------------

Enjoy!
