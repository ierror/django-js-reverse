# -*- coding: utf-8 -*-
import sys
from copy import copy

from django.conf.urls import patterns, url, include


if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

basic_patterns = patterns('',
                          url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

                          # test urls
                          url(r'^test_no_url_args/$', 'foo',
                              name='test_no_url_args'),
                          url(r'^test_one_url_args/(?P<arg_one>[-\w]+)/$', 'foo',
                              name='test_one_url_args'),
                          url(r'^test_two_url_args/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', 'foo',
                              name='test_two_url_args'),
                          url(r'^test_unicode_url_name/$', 'foo',
                              name=u('test_unicode_url_name')))

urlpatterns = copy(basic_patterns)

# test namespace
pattern_ns_1 = patterns('',
                        url(r'', include(basic_patterns)))

pattern_ns_2 = patterns('',
                        url(r'', include(basic_patterns)))

urlpatterns += patterns('',
                        url(r'^ns1/', include(pattern_ns_1, namespace='ns1')),
                        url(r'^ns2/', include(pattern_ns_2, namespace='ns2')))