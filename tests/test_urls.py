# -*- coding: utf-8 -*-
import sys
from copy import copy

from django.conf.urls import include, patterns, url

if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


def dummy_view(*args, **kwargs):
    pass

basic_patterns = patterns('',
                          url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

                          # test urls
                          url(r'^test_no_url_args/$', dummy_view,
                              name='test_no_url_args'),
                          url(r'^test_one_url_args/(?P<arg_one>[-\w]+)/$', dummy_view,
                              name='test_one_url_args'),
                          url(r'^test_two_url_args/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', dummy_view,
                              name='test_two_url_args'),
                          url(r'^test_optional_url_arg/(?:1_(?P<arg_one>[-\w]+)-)?2_(?P<arg_two>[-\w]+)/$', dummy_view,
                              name='test_optional_url_arg'),
                          url(r'^test_unicode_url_name/$', dummy_view,
                              name=u('test_unicode_url_name')),
                          url(r'^test_duplicate_name/(?P<arg_one>[-\w]+)/$', dummy_view,
                              name='test_duplicate_name'),
                          url(r'^test_duplicate_name/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', dummy_view,
                              name='test_duplicate_name'))

urlpatterns = copy(basic_patterns)

# test exclude namespaces urls
urlexclude = patterns('',
                    url(r'^test_exclude_namespace/$', dummy_view,
                            name='test_exclude_namespace_url1'))


# test namespace
pattern_ns_1 = patterns('',
                        url(r'', include(basic_patterns)))

pattern_ns_2 = patterns('',
                        url(r'', include(basic_patterns)))

pattern_ns_arg = patterns('',
                          url(r'', include(basic_patterns)))

pattern_nested_ns = patterns('',
                             url(r'^ns1/', include(pattern_ns_1,
                                                  namespace='ns1')))

urlpatterns += patterns('',
                        url(r'^ns1/', include(pattern_ns_1, namespace='ns1')),
                        url(r'^ns2/', include(pattern_ns_2, namespace='ns2')),
                        url(r'^ns_ex/', include(urlexclude, namespace='exclude_namespace')),
                        url(r'^ns(?P<ns_arg>[^/]*)/', include(pattern_ns_arg, namespace='ns_arg')),
                        url(r'^nestedns/', include(pattern_nested_ns, namespace='nestedns')))
