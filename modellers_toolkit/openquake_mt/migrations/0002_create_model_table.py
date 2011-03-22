# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    def forwards(self, orm):
        db.create_table('openquake_model', (
            ('id', self.gf('django.db.models.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.CharField')(max_length=255,
                                                           unique=True)),
            ('model_type', self.gf('django.db.models.CharField')(max_length=10,
                                                                 editable=True)),
            ('created_at', self.gf('django.db.models.DateTimeField')(auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.DateTimeField')(auto_now=True)),
            ('model_blob', self.gf('django.db.models.TextField')()),
        ))
        db.send_create_signal('openquake_mt', ['Model'])

    def backwards(self, orm):
        # Delete the Model table.
        db.delete_table('openquake_model')

    models = {
        'openquake.model': {
            'Meta': {'object_name': 'Model'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
            },
    }

    complete_apps = ['openquake_mt']
