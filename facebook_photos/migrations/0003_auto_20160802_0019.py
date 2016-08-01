# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_photos', '0002_auto_20160525_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='can_upload',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
