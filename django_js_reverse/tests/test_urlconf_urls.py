from django.views.generic import View
from django.conf.urls import url

urlpatterns = [
    url(r'^test_changed_urlconf/$', View.as_view(), name='test_changed_urlconf'),
]
