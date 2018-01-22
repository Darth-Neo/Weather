from django.conf import settings
from django.conf.urls import include, url
from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r"^list$", ListTemperatureView.as_view(), name="temperature_list",),
    url(r"^new$", CreateTemperatureView.as_view(), name="temperature_new",),
    url(r"^edit/(?P<pk>\d+)/$", EditTemperatureView.as_view(), name="temperature_edit",),
    url(r"^delete/(?P<pk>\d+)/$", DeleteTemperatureView.as_view(), name="temperature_delete",),
    url(r"^(?P<pk>\d+)/$", TemperatureView.as_view(), name="temperature_view",),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]
