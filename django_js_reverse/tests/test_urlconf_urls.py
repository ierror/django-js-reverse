try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url
from django.views.generic import View

urlpatterns = [
    url(r'^test_changed_urlconf/$', View.as_view(), name='test_changed_urlconf'),
]
