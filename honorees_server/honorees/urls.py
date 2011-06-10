from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^honorees.js$', direct_to_template, {'template': 'honorees/honorees.js', 'mimetype': 'text/javascript'}),
    
    url(r'^all_honorees.json$', 'honorees.views.all_honorees'),
    url(r'^all_registrants.json$', 'honorees.views.all_registrants'),
    
    url(r'^honoree/(?P<id>\d+)$', 'honorees.views.honoree'),
    url(r'^registrant/(?P<id>\d+)$', 'honorees.views.registrant'),
    
    url(r'^$', direct_to_template, {'template': 'honorees/index.html'}),
)