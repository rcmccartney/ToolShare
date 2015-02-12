# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserShedAssignation'
        db.delete_table('Sharing_usershedassignation')

        # Adding M2M table for field coordinators on 'Shed'
        m2m_table_name = db.shorten_name('Sharing_shed_coordinators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shed', models.ForeignKey(orm['Sharing.shed'], null=False)),
            ('userprofile', models.ForeignKey(orm['UserAuth.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['shed_id', 'userprofile_id'])


    def backwards(self, orm):
        # Adding model 'UserShedAssignation'
        db.create_table('Sharing_usershedassignation', (
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['UserAuth.UserProfile'], related_name='user_shed_assignments')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('shed', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, to=orm['Sharing.Shed'], related_name='user_shed_assignations')),
        ))
        db.send_create_signal('Sharing', ['UserShedAssignation'])

        # Removing M2M table for field coordinators on 'Shed'
        db.delete_table(db.shorten_name('Sharing_shed_coordinators'))


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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'Sharing.request': {
            'Meta': {'object_name': 'Request', '_ormbases': ['Sharing.Arrangement']},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Sharing.Arrangement']", 'unique': 'True', 'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'Sharing.sharezone': {
            'Meta': {'object_name': 'ShareZone'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'Sharing.sharing': {
            'Meta': {'object_name': 'Sharing', '_ormbases': ['Sharing.Arrangement']},
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Sharing.Arrangement']", 'unique': 'True', 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Sharing.shed': {
            'Meta': {'object_name': 'Shed'},
            'coordinators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'related_name': "'sheds'", 'to': "orm['UserAuth.UserProfile']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['Sharing.ShareZone']", 'null': 'True', 'related_name': "'sheds'"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'UserAuth.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'add_line1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'add_line2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile_photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'reminder_preferences': ('django.db.models.fields.IntegerField', [], {}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['Sharing.ShareZone']", 'null': 'True', 'related_name': "'members'"}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'profile'"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Sharing']