from django.conf.urls import include, url, patterns
from django.contrib import admin

from PratikFizik import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'CRUD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', views.login),
    url(r'^signup', views.signup),
]
