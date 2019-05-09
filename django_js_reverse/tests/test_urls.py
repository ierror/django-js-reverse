# -*- coding: utf-8 -*-
from copy import copy

from django.conf.urls import include as django_include
from django.conf.urls import url
from django.views.generic import View
from django_js_reverse.tests.helper import is_django_ver_gte_2
from django_js_reverse.views import urls_js

try:
    from django.urls import path
except ImportError:
    pass


dummy_view = View.as_view()

basic_patterns = [
    url(r'^jsreverse/$', urls_js, name='js_reverse'),

    # test urls
    url(r'^test_no_url_args/$', dummy_view, name='test_no_url_args'),
    url(r'^test_script/$', dummy_view, name='</script><script>console.log(&amp;)</script><!--'),
    url(r'^test_one_url_args/(?P<arg_one>[-\w]+)/$', dummy_view, name='test_one_url_args'),
    url(r'^test_two_url_args/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', dummy_view, name='test_two_url_args'),
    url(r'^test_optional_url_arg/(?:1_(?P<arg_one>[-\w]+)-)?2_(?P<arg_two>[-\w]+)/$', dummy_view,
        name='test_optional_url_arg'),
    url(r'^test_unicode_url_name/$', dummy_view, name=u'test_unicode_url_name'),
    url(r'^test_duplicate_name/(?P<arg_one>[-\w]+)/$', dummy_view, name='test_duplicate_name'),
    url(r'^test_duplicate_name/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', dummy_view, name='test_duplicate_name'),
    url(r'^test_duplicate_argcount/(?P<arg_one>[-\w]+)?-(?P<arg_two>[-\w]+)?/$', dummy_view,
        name='test_duplicate_argcount'),
]

if is_django_ver_gte_2():
    basic_patterns.append(
        path('test_django_gte_2_path_syntax/<int:arg_one>/<str:arg_two>/', dummy_view,
             name='test_django_gte_2_path_syntax'),
    )

urlpatterns = copy(basic_patterns)

# test exclude namespaces urls
urlexclude = [
    url(r'^test_exclude_namespace/$', dummy_view,
        name='test_exclude_namespace_url1')
]


def include(v, **kwargs):
    if not is_django_ver_gte_2():
        return django_include(v, **kwargs)

    return django_include((v, 'django_js_reverse'), **kwargs)


# test namespace
pattern_ns_1 = [
    url(r'', django_include(basic_patterns))
]

pattern_ns_2 = [
    url(r'', django_include(basic_patterns))
]

pattern_ns = [
    url(r'', django_include(basic_patterns))
]

pattern_nested_ns = [
    url(r'^ns1/', include(pattern_ns_1, namespace='ns1'))
]

pattern_dubble_nested2_ns = [
    url(r'^ns1/', include(pattern_ns_1, namespace='ns1'))]

pattern_dubble_nested_ns = [
    url(r'^ns1/', include(pattern_ns_1, namespace='ns1')),
    url(r'^nsdn2/', include(pattern_dubble_nested2_ns, namespace='nsdn2'))]

pattern_only_nested_ns = [
    url(r'^ns1/', django_include(pattern_ns_1)),
    url(r'^nsdn0/', include(pattern_dubble_nested2_ns, namespace='nsdn0'))]

urlpatterns += [
    url(r'^ns1/', include(pattern_ns_1, namespace='ns1')),
    url(r'^ns2/', include(pattern_ns_2, namespace='ns2')),
    url(r'^ns_ex/', include(urlexclude, namespace='exclude_namespace')),
    url(r'^ns(?P<ns_arg>[^/]*)/', include(pattern_ns, namespace='ns_arg')),
    url(r'^nestedns/', include(pattern_nested_ns, namespace='nestedns')),
    url(r'^nsdn/', include(pattern_dubble_nested_ns, namespace='nsdn')),
    url(r'^nsno/', include(pattern_only_nested_ns, namespace='nsno'))
]
