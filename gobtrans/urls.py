# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from gobtrans.parliament.views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gobtrans.views.home', name='home'),
    # url(r'^gobtrans/', include('gobtrans.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', index),
)
