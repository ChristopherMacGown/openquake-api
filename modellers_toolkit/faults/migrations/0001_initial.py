# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Fault'
        db.create_table('faults_fault', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('faults', ['Fault'])

        # Adding model 'FaultSection'
        db.create_table('faults_faultsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fault', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faults.Fault'])),
            ('slip_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('dip_angel', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('rake_angel', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('faults', ['FaultSection'])


    def backwards(self, orm):
        
        # Deleting model 'Fault'
        db.delete_table('faults_fault')

        # Deleting model 'FaultSection'
        db.delete_table('faults_faultsection')


    models = {
        'faults.fault': {
            'Meta': {'object_name': 'Fault'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'faults.faultsection': {
            'Meta': {'object_name': 'FaultSection'},
            'dip_angel': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'fault': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.Fault']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rake_angel': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'slip_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['faults']
