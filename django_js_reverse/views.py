#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from itertools import chain
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from .settings import JS_VAR_NAME, JS_AVAILABLE_NAMESPACES

def urls_js(request):
    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', JS_VAR_NAME.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (JS_VAR_NAME))

    # Returns list of tuples [(<url_name>, <namespace_path>, <url_patern_tuple> ), ...]
    prepare_url_list = lambda urlresolver, namespace_path='', namespace='': [
        (namespace + url_name, namespace_path, url_pattern[0][0])
        for url_name, url_pattern in urlresolver.reverse_dict.items()
        if (isinstance(url_name, str) or isinstance(url_name, unicode))
    ]

    default_urlresolver = urlresolvers.get_resolver(None)
    # Prepare data for namespeced urls
    named_urlresolves = [
        (n_urlresolver, namespace_path, namespace + ':')
        for namespace, (namespace_path, n_urlresolver) in default_urlresolver.namespace_dict.items()
        if namespace in JS_AVAILABLE_NAMESPACES
    ]

    url_lists = [prepare_url_list(*args) for args in named_urlresolves]
    # Add urls without namespaces
    url_lists.append((prepare_url_list(default_urlresolver)))

    return render_to_response('django_js_reverse/urls_js.tpl',
                              {
                                  'urls': chain(*url_lists),
                                  'url_prefix': urlresolvers.get_script_prefix(),
                                  'js_var_name': JS_VAR_NAME
                              },
                              context_instance=RequestContext(request), mimetype='application/javascript')
