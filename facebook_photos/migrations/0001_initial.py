# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table(u'facebook_photos_album', (
            ('graph_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, max_length=100, primary_key=True)),
            ('author_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('author_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('author_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, db_index=True)),
            ('can_upload', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('cover_photo', self.gf('django.db.models.fields.BigIntegerField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('place', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('privacy', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('type', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
        ))
        db.send_create_signal(u'facebook_photos', ['Album'])

        # Adding model 'Photo'
        db.create_table(u'facebook_photos_photo', (
            ('graph_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, max_length=100, primary_key=True)),
            ('author_json', self.gf('annoying.fields.JSONField')(null=True)),
            ('author_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('author_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, db_index=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', null=True, to=orm['facebook_photos.Album'])),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('picture', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'facebook_photos', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'facebook_photos_album')

        # Deleting model 'Photo'
        db.delete_table(u'facebook_photos_photo')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'facebook_photos.album': {
            'Meta': {'object_name': 'Album'},
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'can_upload': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cover_photo': ('django.db.models.fields.BigIntegerField', [], {}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'graph_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'})
        },
        u'facebook_photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'null': 'True', 'to': u"orm['facebook_photos.Album']"}),
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'graph_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'picture': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['facebook_photos']