from modellers_toolkit.faults.models import Fault, FaultSection, Recurrence, Event, Observation
from modellers_toolkit.faults.models import Fold, FoldTrace
from modellers_toolkit.faults.forms import MAP_OPTIONS, FaultCreationForm, FaultForm, SectionForm, SectionInlineForm, ObservationForm, ObservationInlineForm
from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.admin import OSMGeoAdmin
from django.db import transaction
from olwidget.admin import GeoModelAdmin
from django.forms.models import ModelForm
from olwidget.forms import MapModelForm
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from olwidget.widgets import Map, EditableMap, EditableLayer, InfoLayer
from django.contrib.admin.util import unquote

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
csrf_protect_m = method_decorator(csrf_protect)


class RecurrenceInline(admin.StackedInline):
    model = Recurrence
    extra = 0


class EventInline(admin.StackedInline):
    model = Event
    extra = 0


class ObservationInline(admin.StackedInline):
    """
    Basic admin form for entering observation points.
    
    .. todo:: Allow multiple points to be entered at once.

    """
    model = Observation
    extra = 0
    form = ObservationInlineForm
    readonly_fields = ['fault']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        if 'request' in kwargs:
            del kwargs['request']
        super(ObservationInline, self).__init__(*args, **kwargs)


class SectionInline(admin.StackedInline):
    """Basic admin form for entering and editing Section Traces.
    
    .. todo:: Nested inlines with Recurrence and Events.
    .. todo:: Set fault properly on creation.
    
    """
    model = FaultSection
    extra = 0
    form = SectionInlineForm
    fieldsets = [
        (None,  {'fields': 
            [('fault',), ('expression', 'method', 'activity')],}),
        ('Notes', {'fields': ['notes'], 
            'classes': ['collapse']}),
        ('Geometry', {'fields': 
            ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
            ('dip_angle', 'rake_angle', 'strike_angle'),
            ('upper_depth', 'lower_depth', 'downthrown_side', ),
             'geometry',], 
            'classes' : ['wide', 'show'],}),
    ]
    readonly_fields = ['fault']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        if 'request' in kwargs:
            del kwargs['request']
        super(SectionInline, self).__init__(*args, **kwargs)


class FaultAdmin(GeoModelAdmin):
    """Main admin form for Faults, with inline forms for sections and points.
    
    .. todo:: Filter by active
    
    """
    list_map = ['traces']
    list_map_options = MAP_OPTIONS.copy()
    options = MAP_OPTIONS.copy()
    list_display = ('name', 'completeness', 'last_updated', 'verified_by')
    list_filter = ['completeness', 'verified_by', 'compiler']
    search_fields = ['name', 'notes']
    actions = ['make_verified']
    
    add_form_template = 'admin/faults/add_form.html'
    
    fieldsets = [
         (None,    {'fields': [('name', 'completeness'),]}), 
         ('Provenance', {'fields': [('contributer', 'compiler'), 'notes'], 
            'classes': ['collapse']}), 
    ]
    
    add_fieldsets = (
        (None, {
            'fields': ('name', ),
            'classes': ('wide',)}
        ),
    )
    form = FaultForm
    add_form = FaultCreationForm
    
    readonly_fields = ['compiler',]
    inlines = [ObservationInline, SectionInline]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(FaultAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during Fault creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        form = super(FaultAdmin, self).get_form(request, obj, **defaults)
        return form
    
    def save_model(self, request, obj, form, change):
        if not change: # New Fault
            obj.compiler = request.user
        obj.save()

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        """Suppress all the inlines during add"""
        self.inline_instances = []
        fault = super(FaultAdmin, self).add_view(request, form_url, extra_context)
        for inline_class in self.inlines:
            inline_instance = inline_class(self.model, self.admin_site, request=request)
            self.inline_instances.append(inline_instance)
        return fault
    
    @csrf_protect_m
    @transaction.commit_on_success   
    def change_view(self, request, object_id, extra_context=None):
        print extra_context
        self.inline_instances = []
        for inline_class in self.inlines:
            inline_instance = inline_class(self.model, self.admin_site, request=request)
            obj = self.get_object(request, unquote(object_id))
            inline_instance.form.parent_obj = obj
            self.inline_instances.append(inline_instance)
        fault = super(FaultAdmin, self).change_view(request, object_id, extra_context)
        return fault

    def make_verified(self, request, queryset): 
        if request.user.has_perm('faults.can_verify_faults'):
            rows_updated = queryset.update(verified_by=request.user)
            if rows_updated == 1:
                message_bit = "1 fault was" 
            else:
                message_bit = "%s faults were" % rows_updated
            self.message_user(request, "%s successfully marked as verified." % message_bit)
        else:
            self.message_user(request, "You're not allowed to verify faults, sorry.")
    make_verified.short_description = "Mark selected faults as verified"


class TraceInline(admin.StackedInline):
    model = FoldTrace
    extra = 0
    formfield_overrides = {
        models.LineStringField: 
                {'widget': EditableMap(options={'geometry': 'linestring', 'layers' : ['google.satellite']})},
    }
    fieldsets = [
        (None,  {'fields': 
            [('fold',), ('expression', 'method', 'activity')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'geometry', ], 
            'classes' : ['wide', 'show'],}),
        ('Notes', {'fields': ['notes'], 
            'classes': ['collapse']}),
    ]
    readonly_fields = ['fold']


class FoldAdmin(GeoModelAdmin):
    """Admin form to manage Folds, with inline for fold traces.
    .. todo:: Generalize fieldset and actions for Faults and Folds.
    """
    list_map = ['traces']
    list_map_options = MAP_OPTIONS.copy()
    options = MAP_OPTIONS.copy()
    list_display = ('name', 'completeness', 'last_updated', 'verified_by')
    list_filter = ['completeness', 'verified_by', 'compiler']
    search_fields = ['name', 'notes']
    fieldsets = [
         (None,    {'fields': ['name']}), 
         ('Provenance', {'fields': 
                 [('compiler', 'contributer'),
                 'completeness', ], 'classes': ['collapse']}), 
         ('Details', {'fields': 
                ['notes',],'classes': ['collapse']}),
    ]
    actions = ['make_verified']
    inlines = [TraceInline,]

    def make_verified(self, request, queryset): 
        if request.user.has_perm('faults.can_verify_folds'):
            rows_updated = queryset.update(verified_by=request.user)
            if rows_updated == 1:
                message_bit = "1 fold was" 
            else:
                message_bit = "%s folds were" % rows_updated
            self.message_user(request, "%s successfully marked as verified." % message_bit)
        else:
            self.message_user(request, "You're not allowed to verify folds, sorry.")
    make_verified.short_description = "Mark selected folds as verified"


class SectionAdmin(GeoModelAdmin):
    list_display = ('fault', 'id',)
    list_filter = ['fault']
    list_map = ['geometry']
    list_map_options = MAP_OPTIONS
    options = MAP_OPTIONS
    inlines = [RecurrenceInline, EventInline]
    fieldsets = [
        (None,  {'fields': 
            [('fault',), ('expression', 'method', 'activity')],}),
        ('Geometry', {'fields': 
            ['accuracy', 'aseismic_slip_factor', ('slip_type', 'slip_rate'),
            ('dip_angle', 'rake_angle', 'strike_angle'), 'geometry',
            ('upper_depth', 'lower_depth', 'downthrown_side', )], 'classes' : ['wide', 'show'],}),
        ('Details', {'fields': ['notes'], 'classes': ['collapse']}),
    ]
    form = SectionForm


class ObservationAdmin(GeoModelAdmin):
    list_filter = ['fault']
    list_map = ['geometry']
    list_map_options = MAP_OPTIONS
    options = list_map_options
    form = ObservationForm


admin.site.register(Fault, FaultAdmin)
admin.site.register(Fold, FoldAdmin)
admin.site.register(FaultSection, SectionAdmin)
admin.site.register(Observation, ObservationAdmin)
