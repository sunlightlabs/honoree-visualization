from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.basic_site = admin.AdminSite()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'honorees_server.views.home', name='home'),
    # url(r'^honorees_server/', include('honorees_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.basic_site.urls)),
)
