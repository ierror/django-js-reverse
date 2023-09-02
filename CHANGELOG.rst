0.10.1b1 (unreleased)
---------------------

- Update for Django 4.0 and 4.1, Python 3.8, 3.9, 3.10

0.10.1a1 (unreleased)
---------------------

- Update pypi deploy username and token


0.10.1a (2019-08-02)
--------------------

- support webpack and other bundlers


0.10.0 (2019-08-01)
-------------------

- deprecate django_js_reverse.VERSION. It will now always be ``(0, 9, 2)``
- deprecate js_reverse_inline
- use setuptools.setup

0.9.1
-----

- Fix: avoid XSS introduced in 0.9.0 when using js_reverse_inline. A low threat as content injected is likely to be trusted input from the urlconfig.

0.9.0
-----

- New: Support for Python 3.7
- New: Support for Django 2.2
- New: Unit Tests Script prefix with no slash, changed URL Conf`#72 <https://github.com/ierror/django-js-reverse/issues/72>`__
  Thank you `graingert <https://github.com/graingert>`__
- Fix: "ROOT_URLCONF not taken into account" `#73 <https://github.com/ierror/django-js-reverse/issues/73>`__ `#74 <https://github.com/ierror/django-js-reverse/issues/74>`__
  Thank you `LuukOost <https://github.com/LuukOost>`__ and `graingert <https://github.com/graingert>`__
- Refactoring: "move template logic to view" `#64 <https://github.com/ierror/django-js-reverse/issues/64>`__
  Thank you `graingert <https://github.com/graingert>`__
- Fix: "Now using LooseVersion instead of StrictVersion to avoid issues with rc releases" `#67 <https://github.com/ierror/django-js-reverse/issues/64>`__
  Thank you `kavdev <https://github.com/kavdev>`__

0.8.2
-----

- Fix: A bug fix in Django 2.0.6 has broken django-js-reverse `#65 <https://github.com/ierror/django-js-reverse/issues/65>`_
  Thank you `kavdev <https://github.com/kavdev>`_

0.8.1
-----

- Fix: The tests folder of the `#53 <https://github.com/ierror/django-js-reverse/issues/53>`__ was still present in the build. => Added cleanup to the release make command.

0.8.0
-----

- New: Support for Django 2.0: `#58 <https://github.com/ierror/django-js-reverse/issues/58>`_
  Thank you `wlonk <https://github.com/wlonk>`_
- Fix: `#53 <https://github.com/ierror/django-js-reverse/issues/53>`__ - Don't install the tests folder as a separate folder.  Moved inside the django_js_reverse namespace.

0.7.3
-----

- New: Support for Django 1.10
- Chg: Renamed "production" branch to "master"
- Fix: `#48 <https://github.com/ierror/django-js-reverse/issues/48>`_ - "Change False to 'window' in global object name in README."
  Thank you `karamanolev <https://github.com/karamanolev>`_
- Fix: `PR #45 <https://github.com/ierror/django-js-reverse/pull/45>`_ - "Fix: collectstatic_js_reverse usage message"
  Thank you `ghedsouza <https://github.com/ghedsouza>`_
- Fix: `PR #44 <https://github.com/ierror/django-js-reverse/pull/44>`_ - "Remove duplicate _get_url call"
  Thank you `razh <https://github.com/razh>`_

0.7.2
-----

- Fix: `#42 <https://github.com/ierror/django-js-reverse/issues/42>`_ - "Templatetag js_reverse_inline breaks on Django 1.9"
  Thank you `tommikaikkonen <https://github.com/tommikaikkonen>`_
- Optimized imports

0.7.1
-----
- Fix: `#41 <https://github.com/ierror/django-js-reverse/issues/41>`_ - make it possible to use number 0 as url argument

0.7.0
-----
- New: By default collectstatic_js_reverse writes its output (reverse.js) to your project's STATIC_ROOT. Now You can change settings: JS_REVERSE_OUTPUT_PATH
  Thank you `mjnaderi <https://github.com/ierror/django-js-reverse/pull/36>`__
- New: Support for Django 1.9
  Thank you `mjnaderi <https://github.com/ierror/django-js-reverse/pull/37>`__
- New: It's now possible to include specific namespaces only. See JS_REVERSE_INCLUDE_ONLY_NAMESPACES setting for details.
  Thank you BrnoPCmaniak

0.6.1
-----

- Refactored: Separate the view functionality from the JS generation
- New: Replaced slimit by rjsmin based on `#33 <https://github.com/ierror/django-js-reverse/pull/33/>`_
  Thank you chripede

0.6.0
-----

- Fix: `#27 <https://github.com/ierror/django-js-reverse/pull/27>`_
  Thank you michael-borisov
- New: Support for Keyword-based URL reversing `#30 <https://github.com/ierror/django-js-reverse/pull/30/>`_
  Thank you hyperair

0.5.1
-----

- Fix: Current ply breaks slimit => force ply==3.4

0.5.0
-----

- New: Django allows you to have multiple URL patterns with the same name.
- This release adds support for the featuer.
  Thank you defrex
- New: Test support for django 1.8
- New: test for script_prefix without ending slash

0.4.6
-----

- New: You can change the name (default=this) of the global object the javascript variable used to access the named
  urls is attached to by changing JS_REVERSE_JS_GLOBAL_OBJECT_NAME setting.
  Thank you aumo

0.4.5
-----

- Fix: If you run your application under a subpath, the collectstatic_js_reverse needs to take care of this. You can
  now define a setting JS_REVERSE_SCRIPT_PREFIX that handles this issue.
  Thank you lizter for reporting the issue

0.4.4
-----

- Improvement: management command collectstatic_js_reverse throws an error if settings.STATIC_ROOT is not set
- Tests: exluded a debug print from coverage
- Removed: support for django 1.4
- New: Templatetag to include js-reverse-js inline in your templates

0.4.3
-----

- New: Add better support for django rest framework
  Django rest framework generates url names like user-list, so it get's converted now as well so
  ``Urls['user-list']()`` or the cleaner ``Urls.user_list()`` are both usable.
- Fix: JSReverseStaticFileSaveTest is working and being tested again
- Improvement: Cleanup Javascript
  Thank you bulv1ne for the pull request
- New: Test support for the latest pypy versions pypy3-2.4.0 and pypy-2.5.0
- Fix: Get rid of test warning "MIDDLEWARE_CLASSES is not set." for Django >= 1.7

0.4.2
-----

- Provided PyPI wheel Package

0.4.1
-----

- Fix: collectstatic runner: moved to own management command collectstatic_js_reverse

0.4.0
-----

- Add ability to save in file::

      <script src="{% static 'django_js_reverse/js/reverse.js' %}"></script>``

  to do this run ./manage.py collectstatic

  Add JS_REVERSE_EXCLUDE_NAMESPACES option
  to exclude namespaces from import
  default is []

  To exclude e.g. admin and Django Debug Toolbar::

      JS_REVERSE_EXCLUDE_NAMESPACES = ['admin', 'djdt']

  Thank you Andertaker

0.3.4
-----

- New: Support for nested namespaces. Thank you hyperair
- New: Support for arguments within namespace path. Thank you hyperair
- New: Support for optional url arguments. Thank you hyperair

0.3.3
-----

- New: Django 1.7 support

0.3.2
-----

- New: Default minification of the generated javascript file
- Fix: content type of the jsreverse script. Thank you @emcsween
- Testing: Use selenium for better testing

0.3.1
-----

- Added support for namespaces

0.3.0
-----

- Test support for pypy, python 3.4, django 1.6
- Refactored include of JS_REVERSE_JS_VAR_NAME js var name
- Get rid of "DeprecationWarning: The mimetype keyword argument is depracated, use content_type instead"
