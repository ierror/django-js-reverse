#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from .settings import JS_VAR_NAME


def urls_js(request):
    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', JS_VAR_NAME.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (JS_VAR_NAME))

    url_patterns = list(urlresolvers.get_resolver(None).reverse_dict.items())
    url_list = [(url_name, url_pattern[0][0]) for url_name, url_pattern in url_patterns if
                isinstance(url_name, str)]

    return render_to_response('django_js_reverse/urls_js.tpl',
                              {
                                  'urls': url_list,
                                  'url_prefix': urlresolvers.get_script_prefix(),
                                  'js_var_name': JS_VAR_NAME
                              },
                              context_instance=RequestContext(request), mimetype='application/javascript'
    )
