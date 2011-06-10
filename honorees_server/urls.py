from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('',
    url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'', include('honorees.urls')),
)
