from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import temperature.views
# import aprs_message.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',    temperature.views.ListTemperatureView.as_view(), name='temperature_list',),
    url(r'^list$',    temperature.views.ListTemperatureView.as_view(), name='temperature_list',),

    url(r'^new$', temperature.views.CreateTemperatureView.as_view(), name='temperature_new',),
    url(r'^edit/(?P<pk>\d+)/$', temperature.views.UpdateTemperatureView.as_view(), name='temperature_edit',),
    url(r'^delete/(?P<pk>\d+)/$', temperature.views.DeleteTemperatureView.as_view(), name='temperature_delete',),

    url(r'^(?P<pk>\d+)/$', temperature.views.TemperatureView.as_view(), name='temperature_view',),
    url(r'^charts/simple.png$', 'temperature.charts.simple'),
)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)),
    )

urlpatterns += staticfiles_urlpatterns()

