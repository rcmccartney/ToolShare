# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ToolCategory'
        db.create_table('ToolMgmt_toolcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('ToolMgmt', ['ToolCategory'])

        # Adding model 'ToolStatus'
        db.create_table('ToolMgmt_toolstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('ToolMgmt', ['ToolStatus'])

        # Adding model 'Tool'
        db.create_table('ToolMgmt_tool', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ToolMgmt.ToolCategory'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ToolMgmt.ToolStatus'])),
        ))
        db.send_create_signal('ToolMgmt', ['Tool'])


    def backwards(self, orm):
        # Deleting model 'ToolCategory'
        db.delete_table('ToolMgmt_toolcategory')

        # Deleting model 'ToolStatus'
        db.delete_table('ToolMgmt_toolstatus')

        # Deleting model 'Tool'
        db.delete_table('ToolMgmt_tool')


    models = {
        'ToolMgmt.tool': {
            'Meta': {'object_name': 'Tool'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ToolMgmt.ToolCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ToolMgmt.ToolStatus']"})
        },
        'ToolMgmt.toolcategory': {
            'Meta': {'object_name': 'ToolCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ToolMgmt.toolstatus': {
            'Meta': {'object_name': 'ToolStatus'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['ToolMgmt']