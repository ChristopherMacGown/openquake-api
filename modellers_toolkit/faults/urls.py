from django.conf.urls.defaults import *
from django.contrib import databrowse

from modellers_toolkit.faults import models

databrowse.site.register(models.Fault)
databrowse.site.register(models.FaultSection)
databrowse.site.register(models.Observation)
databrowse.site.register(models.Fold)
databrowse.site.register(models.FoldTrace)

urlpatterns = patterns('',
)
