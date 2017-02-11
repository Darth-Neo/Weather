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
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^temperature/', include("temperature.urls")),
    url(r'^$', include("temperature.urls")),
)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)),
    )

urlpatterns += staticfiles_urlpatterns()

