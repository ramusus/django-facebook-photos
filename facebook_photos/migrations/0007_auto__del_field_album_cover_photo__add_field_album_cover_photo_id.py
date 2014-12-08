# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Album.cover_photo'
        db.delete_column(u'facebook_photos_album', 'cover_photo')

        # Adding field 'Album.cover_photo_id'
        db.add_column(u'facebook_photos_album', 'cover_photo_id',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Album.cover_photo'
        db.add_column(u'facebook_photos_album', 'cover_photo',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Album.cover_photo_id'
        db.delete_column(u'facebook_photos_album', 'cover_photo_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'facebook_comments.comment': {
            'Meta': {'object_name': 'Comment'},
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_authors_comments'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'can_remove': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'likes_users': ('m2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'like_comments'", 'symmetrical': 'False', 'to': u"orm['facebook_users.User']"}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_owners_comments'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'owner_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'user_likes': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'facebook_photos.album': {
            'Meta': {'object_name': 'Album'},
            'actions_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_authors_albums'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'can_upload': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'cover_photo_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'graph_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'likes_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'likes_users': ('m2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'like_albums'", 'symmetrical': 'False', 'to': u"orm['facebook_users.User']"}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_owners_albums'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'owner_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'photos_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'place': ('annoying.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'shares_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'shares_users': ('m2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'shares_albums'", 'symmetrical': 'False', 'to': u"orm['facebook_users.User']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'})
        },
        u'facebook_photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'actions_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'null': 'True', 'to': u"orm['facebook_photos.Album']"}),
            'author_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_authors_photos'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'author_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'author_json': ('annoying.fields.JSONField', [], {'null': 'True'}),
            'comments_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'graph_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'likes_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'likes_users': ('m2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'like_photos'", 'symmetrical': 'False', 'to': u"orm['facebook_users.User']"}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'picture': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'place': ('annoying.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'shares_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'shares_users': ('m2m_history.fields.ManyToManyHistoryField', [], {'related_name': "'shares_photos'", 'symmetrical': 'False', 'to': u"orm['facebook_users.User']"}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        u'facebook_users.user': {
            'Meta': {'object_name': 'User'},
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
            'graph_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'}),
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