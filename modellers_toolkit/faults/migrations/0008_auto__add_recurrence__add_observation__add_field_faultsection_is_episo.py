# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Recurrence'
        db.create_table('faults_recurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dip_slip_ratio', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('marker_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('scaling', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('faults', ['Recurrence'])

        # Adding model 'Observation'
        db.create_table('faults_observation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fault', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faults.Fault'])),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('faults', ['Observation'])

        # Adding field 'FaultSection.is_episodic'
        db.add_column('faults_faultsection', 'is_episodic', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'FaultSection.is_active'
        db.add_column('faults_faultsection', 'is_active', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Recurrence'
        db.delete_table('faults_recurrence')

        # Deleting model 'Observation'
        db.delete_table('faults_observation')

        # Deleting field 'FaultSection.is_episodic'
        db.delete_column('faults_faultsection', 'is_episodic')

        # Deleting field 'FaultSection.is_active'
        db.delete_column('faults_faultsection', 'is_active')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'faults.fault': {
            'Meta': {'object_name': 'Fault'},
            'compiler': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'completeness': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'contributer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'faults.faultsection': {
            'Meta': {'object_name': 'FaultSection'},
            'dip_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'fault': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.Fault']"}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_episodic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lower_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'rake_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'slip_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'upper_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'faults.fold': {
            'Meta': {'object_name': 'Fold'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'faults.foldsection': {
            'Meta': {'object_name': 'FoldSection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'faults.observation': {
            'Meta': {'object_name': 'Observation'},
            'fault': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.Fault']"}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'faults.recurrence': {
            'Meta': {'object_name': 'Recurrence'},
            'dip_slip_ratio': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marker_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scaling': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['faults']
