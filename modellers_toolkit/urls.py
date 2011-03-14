from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.static import serve
from django.contrib import databrowse

from django.contrib import admin

from modellers_toolkit.faults import urls as faulturls
from modellers_toolkit.openquake_mt import urls as openquakeurls
from modellers_toolkit.api import urls as apiurls

admin.autodiscover()

urlpatterns = patterns('',
    (r'^faults/', include(faulturls)),
    (r'^jobs/', include(openquakeurls)),
    (r'^api/', include(apiurls)),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^admin/', include(admin.site.urls)),
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 
            serve, {'document_root': settings.MEDIA_ROOT}), 
    (r'^', direct_to_template, {'template': 'welcome.html'}),
)
