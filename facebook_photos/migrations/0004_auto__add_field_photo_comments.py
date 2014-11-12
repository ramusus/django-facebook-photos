# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.comments'
        db.add_column('vkontakte_photos_photo', 'comments',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Photo.comments'
        db.delete_column('vkontakte_photos_photo', 'comments')

    models = {
        'vkontakte_groups.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_big': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vkontakte_users.User']", 'symmetrical': 'False'})
        },
        'vkontakte_photos.album': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Album'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_albums'", 'null': 'True', 'to': "orm['vkontakte_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photo_albums'", 'null': 'True', 'to': "orm['vkontakte_users.User']"}),
            'privacy': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'20'"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'thumb_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'thumb_src': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'vkontakte_photos.photo': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['vkontakte_photos.Album']"}),
            'comments': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'null': 'True', 'to': "orm['vkontakte_groups.Group']"}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'null': 'True', 'to': "orm['vkontakte_users.User']"}),
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'20'"}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'src_big': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'src_small': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'src_xbig': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'src_xxbig': ('django.db.models.fields.CharField', [], {'max_length': "'200'"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos_author'", 'to': "orm['vkontakte_users.User']"}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'vkontakte_places.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'null': 'True', 'to': "orm['vkontakte_places.Country']"}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_places.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_users.user': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'User'},
            'activity': ('django.db.models.fields.TextField', [], {}),
            'albums': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'audios': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bdate': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.City']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'counters_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.Country']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'faculty': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'faculty_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'friends': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'graduation': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'has_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mutual_friends': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_big': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium_rec': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_rec': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'relation': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'subscriptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sum_counters': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'university': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'university_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user_photos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user_videos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'videos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'wall_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['vkontakte_photos']