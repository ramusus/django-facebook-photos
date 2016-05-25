# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_photos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='cover_photo_id',
        ),
        migrations.AddField(
            model_name='album',
            name='cover_photo',
            field=models.ForeignKey(related_name='cover_for_albums', to='facebook_photos.Photo', null=True),
            preserve_default=True,
        ),
    ]
