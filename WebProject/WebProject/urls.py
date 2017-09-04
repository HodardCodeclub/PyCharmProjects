from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('WebApp.views',
                       url(r'^$', 'hello'),
                       url(r'^login$', 'login'),
                       url(r'^signup$', 'signup'),
                       url(r'^accounts/', 'account'),
                       url(r'^readAll$', 'readAll'),
                       url(r'^clear$', 'deleteAll'),)
