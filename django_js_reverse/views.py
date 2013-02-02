#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers


def urls_js(request):
    url_patterns = urlresolvers.get_resolver(None).reverse_dict.items()
    url_list = [(url_name, url_pattern[0][0]) for url_name, url_pattern in url_patterns if isinstance(url_name, basestring)]
    return render_to_response('django_js_reverse/urls_js.tpl',
        {
            'urls': url_list
        },
        context_instance=RequestContext(request), mimetype='application/javascript'
    )