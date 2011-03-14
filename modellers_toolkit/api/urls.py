from django.conf.urls.defaults import *
from piston import resource
from modellers_toolkit.api import handlers


job_resource = resource.Resource(handlers.JobHandler)

urlpatterns = patterns('',
    url(r'^jobs/(?P<id>\w+)$', job_resource),
    url(r'^jobs$', job_resource),
)
