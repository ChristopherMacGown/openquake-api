from django.contrib import admin
from modellers_toolkit.openquake_mt import models as openquake_models


class JobAdmin(admin.ModelAdmin):
    fields = ['name', 'repo']
    list_display = ('name', 'status', 'created_at', 'updated_at')

class ModelAdmin(admin.ModelAdmin):
    fields = ['name', 'model_blob', 'model_type']
    list_display = ('name', 'created_at', 'updated_at')


admin.site.register(openquake_models.Job, JobAdmin)
admin.site.register(openquake_models.Model, ModelAdmin)
