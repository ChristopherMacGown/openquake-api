import functools

import olwidget

from models import FaultSection, Fault, Observation
from django import forms
from django.forms.models import ModelForm
from django.contrib.admin.helpers import InlineAdminForm, AdminForm

from olwidget.forms import MapModelForm
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from olwidget.widgets import EditableLayer, InfoLayer, Map

from django.contrib.gis.db.models.fields import LineStringField

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.formtools.wizard import FormWizard

from modellers_toolkit.faults import classmaker


MAP_OPTIONS = {
        'default_lat' : -41.215,
        'default_lon' : 174.897, 
        'default_zoom' : 10,
        'layers' : ['google.satellite', 've.aerial', 'osm.osmarender'],
        'zoom_to_data_extent' : True,
        'popups_outside' : True,
        'map_options' : { 
                'controls' : 
                ['LayerSwitcher', 'Navigation', 'PanZoomBar', 'Attribution'], 
                'min_extent' : 'new OpenLayers.Bounds(-10, -10, 10, 10)'},
        'min_extent' : 'new OpenLayers.Bounds(-10, -10, 10, 10)',
}


class FaultForm(ModelForm):
    """Main form for editing existing Faults."""
    class Meta:
        model = Fault


class FaultCreationForm(ModelForm):
    """A form that creates a Fault, with no sections."""
    name = forms.CharField(label=_("Name of Fault"))

    class Meta:
        model = Fault
        fields = ("name",)

    def save(self, commit=True):
        fault = super(FaultCreationForm, self).save(commit=False)
        if commit:
            fault.save()
        return fault


def make_section_layer(fault, section_id):
    return InfoLayerField([[s.geometry, "%s Sections" % (s.__unicode__())]
            for s in fault.faultsection_set.filter(
            geometry__isnull=False).exclude(id=section_id)],
            {
                    'geometry': 'linestring',
                    'overlay_style': {
                        'fill_opacity': 0,
                        'stroke_color': "grey",
                        'stroke_width': 2,
                    }, 
                    'name': "Other Sections",
            }) 
              
                    
def make_point_layer(fault, observation_id):
    return InfoLayerField([[o.geometry, "%s Observations" % (o.__unicode__())]
            for o in fault.observation_set.filter(
            geometry__isnull=False).exclude(id=observation_id)],
            {
                'geometry': 'point',
                'overlay_style': {                             
                    'externalGraphic': "/media/alien.png",
                    'graphicWidth': 21,
                    'graphicHeight': 25,
                }, 
                'name': "Observations",
            })


class SectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        layers = [EditableLayerField({'geometry': 'linestring', 'name': 'geometry'})]
        if hasattr(self.instance, 'fault'):
            layers.append(make_section_layer(self.instance.fault, self.instance.id))
            layers.append(make_point_layer(self.instance.fault, None))
        self.fields['geometry'] = olwidget.fields.MapField(layers, MAP_OPTIONS)


class SectionInlineForm(ModelForm, MapModelForm):
    """FaultSection creation and editing, used both in dedicated and inline views."""
    __metaclass__ = classmaker()
    parent_obj = None
    
    def __init__(self, *args, **kwargs):
        super(SectionInlineForm, self).__init__(*args, **kwargs)
        self.set_layers()
    
    def set_layers(self):
        fault = self.__class__.parent_obj # Can use self.instance sometimes?
        layers = [EditableLayerField({'geometry': 'linestring', 'name': 'geometry'})]
        layers.append(make_section_layer(fault, self.instance.id))
        layers.append(make_point_layer(fault, None))
        self.fields['geometry'] = olwidget.fields.MapField(layers, MAP_OPTIONS)
    
    class Meta:
        model = FaultSection


class ObservationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ObservationForm, self).__init__(*args, **kwargs)
        self.set_layers()
    
    def set_layers(self):
        layers = [EditableLayerField({'geometry': 'point', 'name': 'geometry'})]
        if hasattr(self.instance, 'fault'):
            layers.append(make_section_layer(self.instance.fault, None))
            layers.append(make_point_layer(self.instance.fault, self.instance.id))
        self.fields['geometry'] = olwidget.fields.MapField(layers, MAP_OPTIONS)
    

class ObservationInlineForm(ModelForm, MapModelForm):
    __metaclass__ = classmaker()
    parent_obj = None
    
    def __init__(self, *args, **kwargs):
        super(ObservationInlineForm, self).__init__(*args, **kwargs)
        self.set_layers()
        
    def set_layers(self):   
        fault = self.__class__.parent_obj # Can use self.instance sometimes?     
        layers = [EditableLayerField({'geometry': 'point', 'name': 'geometry'})]
        layers.append(make_section_layer(fault, None))
        layers.append(make_point_layer(fault, self.instance.id))
        self.fields['geometry'] = olwidget.fields.MapField(layers, MAP_OPTIONS)
    
    class Meta:
        model = Observation
