# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'FaultSection.rake_angel'
        db.delete_column('faults_faultsection', 'rake_angel')

        # Deleting field 'FaultSection.dip_angel'
        db.delete_column('faults_faultsection', 'dip_angel')

        # Adding field 'FaultSection.dip_angle'
        db.add_column('faults_faultsection', 'dip_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2), keep_default=False)

        # Adding field 'FaultSection.rake_angle'
        db.add_column('faults_faultsection', 'rake_angle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2), keep_default=False)

        # Adding field 'FaultSection.geometry'
        db.add_column('faults_faultsection', 'geometry', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'FaultSection.upper_depth'
        db.add_column('faults_faultsection', 'upper_depth', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2), keep_default=False)

        # Adding field 'FaultSection.lower_depth'
        db.add_column('faults_faultsection', 'lower_depth', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2), keep_default=False)

        # Changing field 'FaultSection.slip_rate'
        db.alter_column('faults_faultsection', 'slip_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2))

        # Adding field 'Fault.compiler'
        db.add_column('faults_fault', 'compiler', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)

        # Adding field 'Fault.contributer'
        db.add_column('faults_fault', 'contributer', self.gf('django.db.models.fields.CharField')(default='GEM Faulted Earth', max_length=255), keep_default=False)

        # Adding field 'Fault.created_at'
        db.add_column('faults_fault', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2010, 12, 12), blank=True), keep_default=False)

        # Adding field 'Fault.last_updated'
        db.add_column('faults_fault', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2010, 12, 12), blank=True), keep_default=False)

        # Adding field 'Fault.completeness'
        db.add_column('faults_fault', 'completeness', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'FaultSection.rake_angel'
        raise RuntimeError("Cannot reverse this migration. 'FaultSection.rake_angel' and its values cannot be restored.")


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
            'completeness': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'contributer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'faults.faultsection': {
            'Meta': {'object_name': 'FaultSection'},
            'dip_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'fault': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.Fault']"}),
            'geometry': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lower_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'rake_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'slip_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'upper_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['faults']
