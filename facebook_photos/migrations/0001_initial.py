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
            ('can_upload', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('cover_photo', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('place', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('privacy', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('type', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photo_albums', null=True, to=orm['facebook_users.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='200')),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('updated_time', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
        ))
        db.send_create_signal(u'facebook_photos', ['Album'])

        # Adding model 'Photo'
        db.create_table(u'facebook_photos_photo', (
            ('graph_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, max_length=100, primary_key=True)),
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

        # Adding model 'Comment'
        db.create_table(u'facebook_photos_comment', (
            ('graph_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, max_length=100, primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length='20')),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['facebook_photos.Photo'])),
            ('author_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photo_comments', to=orm['contenttypes.ContentType'])),
            ('author_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'facebook_photos', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'facebook_photos_album')

        # Deleting model 'Photo'
        db.delete_table(u'facebook_photos_photo')

        # Deleting model 'Comment'
        db.delete_table(u'facebook_photos_comment')


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
            'can_upload': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cover_photo': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'graph_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_albums'", 'null': 'True', 'to': u"orm['facebook_users.User']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'})
        },
        u'facebook_photos.comment': {
            'Meta': {'object_name': 'Comment'},
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_comments'", 'to': u"orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'graph_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['facebook_photos.Photo']"}),
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'20'"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'facebook_photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'null': 'True', 'to': u"orm['facebook_photos.Album']"}),
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
        },
        u'facebook_users.user': {
            'Meta': {'ordering': "['graph_id']", 'object_name': 'User'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'cover': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'currency': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'devices': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'education': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'favorite_athletes': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'favorite_teams': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'hometown': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installed': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'interested_in': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'languages': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'location': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'payment_pricepoints': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'picture': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'political': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quotes': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'relationship_status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'security_settings': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'significant_other': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'third_party_id': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_upload_limits': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '100'}),
            'work': ('annoying.fields.JSONField', [], {'max_length': '500', 'null': 'True'})
        }
    }

    complete_apps = ['facebook_photos']