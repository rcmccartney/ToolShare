# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShareZone'
        db.create_table('Sharing_sharezone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Sharing', ['ShareZone'])

        # Adding model 'Shed'
        db.create_table('Sharing_shed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sharezone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sharing.ShareZone'], null=True, blank=True, related_name='sheds')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Sharing', ['Shed'])

        # Adding model 'UserShedAssignation'
        db.create_table('Sharing_usershedassignation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['UserAuth.UserProfile'], related_name='user_shed_assignments')),
            ('shed', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['Sharing.Shed'], related_name='user_shed_assignations')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Sharing', ['UserShedAssignation'])

        # Adding model 'Arrangement'
        db.create_table('Sharing_arrangement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('pickup_arrangement', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('borrower', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['UserAuth.UserProfile'], related_name='borrowers')),
            ('lender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['UserAuth.UserProfile'], related_name='lenders')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Sharing', ['Arrangement'])

        # Adding model 'Sharing'
        db.create_table('Sharing_sharing', (
            ('arrangement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Sharing.Arrangement'], primary_key=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('returned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Sharing', ['Sharing'])

        # Adding model 'Request'
        db.create_table('Sharing_request', (
            ('arrangement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Sharing.Arrangement'], primary_key=True)),
            ('msg', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Sharing', ['Request'])


    def backwards(self, orm):
        # Deleting model 'ShareZone'
        db.delete_table('Sharing_sharezone')

        # Deleting model 'Shed'
        db.delete_table('Sharing_shed')

        # Deleting model 'UserShedAssignation'
        db.delete_table('Sharing_usershedassignation')

        # Deleting model 'Arrangement'
        db.delete_table('Sharing_arrangement')

        # Deleting model 'Sharing'
        db.delete_table('Sharing_sharing')

        # Deleting model 'Request'
        db.delete_table('Sharing_request')


    models = {
        'Sharing.arrangement': {
            'Meta': {'object_name': 'Arrangement'},
            'borrower': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['UserAuth.UserProfile']", 'related_name': "'borrowers'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['UserAuth.UserProfile']", 'related_name': "'lenders'"}),
            'pickup_arrangement': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'Sharing.request': {
            'Meta': {'object_name': 'Request', '_ormbases': ['Sharing.Arrangement']},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Sharing.Arrangement']", 'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'Sharing.sharezone': {
            'Meta': {'object_name': 'ShareZone'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'Sharing.sharing': {
            'Meta': {'object_name': 'Sharing', '_ormbases': ['Sharing.Arrangement']},
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Sharing.Arrangement']", 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Sharing.shed': {
            'Meta': {'object_name': 'Shed'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Sharing.ShareZone']", 'null': 'True', 'blank': 'True', 'related_name': "'sheds'"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'Sharing.usershedassignation': {
            'Meta': {'object_name': 'UserShedAssignation'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shed': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['Sharing.Shed']", 'related_name': "'user_shed_assignations'"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['UserAuth.UserProfile']", 'related_name': "'user_shed_assignments'"})
        },
        'UserAuth.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'add_line1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'add_line2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile_photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'reminder_preferences': ('django.db.models.fields.IntegerField', [], {}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Sharing.ShareZone']", 'null': 'True', 'blank': 'True', 'related_name': "'members'"}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']", 'related_name': "'profile'"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Sharing']