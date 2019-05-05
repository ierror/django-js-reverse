from django.conf.urls import url
from django.views.generic import View

urlpatterns = [
    url(r'^test_changed_urlconf/$', View.as_view(), name='test_changed_urlconf'),
]
