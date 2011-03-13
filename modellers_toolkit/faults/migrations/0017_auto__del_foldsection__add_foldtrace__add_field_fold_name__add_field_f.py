# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'FoldSection'
        db.delete_table('faults_foldsection')

        # Adding model 'FoldTrace'
        db.create_table('faults_foldtrace', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_episodic', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fold', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faults.Fold'])),
            ('method', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('expression', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('accuracy', self.gf('django.db.models.fields.DecimalField')(default=0.10000000000000001, max_digits=3, decimal_places=2)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.LineStringField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('dip_axial_plane', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('dip_dir_shallow_limb', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('dip_dir_steep_limb', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('dip_shallow_limb', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('dip_steep_limb', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('growth_horizontal', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('growth_vertical', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('plunge', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('plunge_dir', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('surface_age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tilt_shallow_limb', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('tilt_steep_limb', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('fold_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('faults', ['FoldTrace'])

        # Adding field 'Fold.name'
        db.add_column('faults_fold', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'Fold.compiler'
        db.add_column('faults_fold', 'compiler', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']), keep_default=False)

        # Adding field 'Fold.contributer'
        db.add_column('faults_fold', 'contributer', self.gf('django.db.models.fields.CharField')(default='GEM Faulted Earth', max_length=255), keep_default=False)

        # Adding field 'Fold.created_at'
        db.add_column('faults_fold', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.date(2010, 12, 16), blank=True), keep_default=False)

        # Adding field 'Fold.last_updated'
        db.add_column('faults_fold', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2010, 12, 16), blank=True), keep_default=False)

        # Adding field 'Fold.completeness'
        db.add_column('faults_fold', 'completeness', self.gf('django.db.models.fields.IntegerField')(default=4), keep_default=False)

        # Adding field 'Fold.notes'
        db.add_column('faults_fold', 'notes', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Fold.verified_by'
        db.add_column('faults_fold', 'verified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='faults_fold_verifier', null=True, to=orm['auth.User']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'FoldSection'
        db.create_table('faults_foldsection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('faults', ['FoldSection'])

        # Deleting model 'FoldTrace'
        db.delete_table('faults_foldtrace')

        # Deleting field 'Fold.name'
        db.delete_column('faults_fold', 'name')

        # Deleting field 'Fold.compiler'
        db.delete_column('faults_fold', 'compiler_id')

        # Deleting field 'Fold.contributer'
        db.delete_column('faults_fold', 'contributer')

        # Deleting field 'Fold.created_at'
        db.delete_column('faults_fold', 'created_at')

        # Deleting field 'Fold.last_updated'
        db.delete_column('faults_fold', 'last_updated')

        # Deleting field 'Fold.completeness'
        db.delete_column('faults_fold', 'completeness')

        # Deleting field 'Fold.notes'
        db.delete_column('faults_fold', 'notes')

        # Deleting field 'Fold.verified_by'
        db.delete_column('faults_fold', 'verified_by_id')


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
        'faults.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'historical_eq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prehistorical_eq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.FaultSection']"})
        },
        'faults.fault': {
            'Meta': {'object_name': 'Fault'},
            'compiler': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']"}),
            'completeness': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'contributer': ('django.db.models.fields.CharField', [], {'default': "'GEM Faulted Earth'", 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'verified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faults_fault_verifier'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'faults.faultsection': {
            'Meta': {'object_name': 'FaultSection'},
            'accuracy': ('django.db.models.fields.DecimalField', [], {'default': '0.10000000000000001', 'max_digits': '3', 'decimal_places': '2'}),
            'aseismic_slip_factor': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'dip_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'downthrown_side': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '2'}),
            'expression': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'fault': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.Fault']"}),
            'geometry': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_episodic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lower_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'method': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'rake_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'slip_rate': ('django.db.models.fields.IntegerField', [], {'default': '3', 'null': 'True'}),
            'slip_type': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'strike_angle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'upper_depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'faults.fold': {
            'Meta': {'object_name': 'Fold'},
            'compiler': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']"}),
            'completeness': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'contributer': ('django.db.models.fields.CharField', [], {'default': "'GEM Faulted Earth'", 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'verified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faults_fold_verifier'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'faults.foldtrace': {
            'Meta': {'object_name': 'FoldTrace'},
            'accuracy': ('django.db.models.fields.DecimalField', [], {'default': '0.10000000000000001', 'max_digits': '3', 'decimal_places': '2'}),
            'dip_axial_plane': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'dip_dir_shallow_limb': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'dip_dir_steep_limb': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'dip_shallow_limb': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'dip_steep_limb': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'expression': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'fold': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.Fold']"}),
            'fold_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'geometry': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True', 'blank': 'True'}),
            'growth_horizontal': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'growth_vertical': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_episodic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'method': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'plunge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'plunge_dir': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'surface_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tilt_shallow_limb': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'tilt_steep_limb': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
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
            'earthquake': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'marker_age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scaling': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faults.FaultSection']"})
        }
    }

    complete_apps = ['faults']
