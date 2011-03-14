# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding Job Model
        db.create_table('openquake_job', (
            ('id', self.gf('django.db.models.AutoField')(primary_key=True)),
            ('job_hash', self.gf('django.db.models.CharField')(max_length=40,
                                                               editable=False)),
            ('created_at', self.gf('django.db.models.DateTimeField')(auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.DateTimeField')(auto_now=True)),
            ('status', self.gf('django.db.models.CharField')(max_length=10, 
                                                             editable=False,
                                                             default='new')),
            ('name', self.gf('django.db.models.CharField')(max_length=255, 
                                                           unique=True)),
            ('repo', self.gf('django.db.models.URLField')(max_length=200)),
        ))
        db.send_create_signal('openquake_mt', ['Job'])

    def backwards(self, orm):
        # Deleting Job Model
        db.delete_table('openquake_job')

    models = {
        'openquake.job': {
            'Meta': {'object_name': 'Job'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
            },
    }

    complete_apps = ['openquake_mt']
