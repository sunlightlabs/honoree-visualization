from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^honorees.js$', direct_to_template, {'template': 'honorees/honorees.js', 'mimetype': 'text/javascript'}),
    
    url(r'^all_honorees.json$', 'honorees.views.all_honorees'),
    url(r'^all_registrants.json$', 'honorees.views.all_registrants'),
    
    url(r'^(?P<type>(registrant|honoree))/(?P<id>\d+).json$', 'honorees.views.entity'),
    
    url(r'^$', direct_to_template, {'template': 'honorees/index.html'}),
)