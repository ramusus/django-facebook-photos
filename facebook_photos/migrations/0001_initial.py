# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import m2m_history.fields
import facebook_api.models
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_users', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('graph_id', models.BigIntegerField(help_text='Unique graph ID', serialize=False, verbose_name='ID', primary_key=True)),
                ('owner_id', models.BigIntegerField(null=True, db_index=True)),
                ('author_json', annoying.fields.JSONField(help_text=b'Information about the user who posted the message', null=True)),
                ('author_id', models.BigIntegerField(null=True, db_index=True)),
                ('actions_count', models.PositiveIntegerField(help_text=b'The number of total actions with this item', null=True)),
                ('likes_count', models.PositiveIntegerField(help_text=b'The number of likes of this item', null=True)),
                ('shares_count', models.PositiveIntegerField(help_text=b'The number of shares of this item', null=True)),
                ('comments_count', models.PositiveIntegerField(help_text=b'The number of comments of this item', null=True)),
                ('can_upload', models.NullBooleanField()),
                ('photos_count', models.PositiveIntegerField(null=True)),
                ('cover_photo_id', models.BigIntegerField(null=True)),
                ('link', models.URLField(max_length=255)),
                ('location', models.CharField(max_length=200)),
                ('place', annoying.fields.JSONField(null=True, blank=True)),
                ('privacy', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(null=True, db_index=True)),
                ('updated_time', models.DateTimeField(null=True, db_index=True)),
                ('author_content_type', models.ForeignKey(related_name='content_type_authors_facebook_photos_albums', to='contenttypes.ContentType', null=True)),
                ('likes_users', m2m_history.fields.ManyToManyHistoryField(related_name='like_albums', to='facebook_users.User')),
                ('owner_content_type', models.ForeignKey(related_name='content_type_owners_facebook_photos_albums', to='contenttypes.ContentType', null=True)),
                ('shares_users', m2m_history.fields.ManyToManyHistoryField(related_name='shares_albums', to='facebook_users.User')),
            ],
            options={
                'verbose_name': 'Facebook Album',
                'verbose_name_plural': 'Facebook Albums',
            },
            bases=(facebook_api.models.FacebookGraphPKModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('graph_id', models.BigIntegerField(help_text='Unique graph ID', serialize=False, verbose_name='ID', primary_key=True)),
                ('author_json', annoying.fields.JSONField(help_text=b'Information about the user who posted the message', null=True)),
                ('author_id', models.BigIntegerField(null=True, db_index=True)),
                ('actions_count', models.PositiveIntegerField(help_text=b'The number of total actions with this item', null=True)),
                ('likes_count', models.PositiveIntegerField(help_text=b'The number of likes of this item', null=True)),
                ('shares_count', models.PositiveIntegerField(help_text=b'The number of shares of this item', null=True)),
                ('comments_count', models.PositiveIntegerField(help_text=b'The number of comments of this item', null=True)),
                ('link', models.URLField(max_length=255)),
                ('picture', models.URLField(max_length=255)),
                ('source', models.URLField(max_length=255)),
                ('name', models.TextField()),
                ('place', annoying.fields.JSONField(null=True, blank=True)),
                ('width', models.PositiveIntegerField(null=True)),
                ('height', models.PositiveIntegerField(null=True)),
                ('created_time', models.DateTimeField(null=True, db_index=True)),
                ('updated_time', models.DateTimeField(null=True, db_index=True)),
                ('album', models.ForeignKey(related_name='photos', to='facebook_photos.Album', null=True)),
                ('author_content_type', models.ForeignKey(related_name='content_type_authors_facebook_photos_photos', to='contenttypes.ContentType', null=True)),
                ('likes_users', m2m_history.fields.ManyToManyHistoryField(related_name='like_photos', to='facebook_users.User')),
                ('shares_users', m2m_history.fields.ManyToManyHistoryField(related_name='shares_photos', to='facebook_users.User')),
            ],
            options={
                'verbose_name': 'Facebook Photo',
                'verbose_name_plural': 'Facebook Photos',
            },
            bases=(facebook_api.models.FacebookGraphPKModelMixin, models.Model),
        ),
    ]
