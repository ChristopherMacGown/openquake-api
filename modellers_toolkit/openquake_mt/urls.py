from django.conf.urls.defaults import *
from django.contrib import databrowse

from modellers_toolkit.openquake_mt import models

databrowse.site.register(models.Job)

urlpatterns = patterns('',
)
