# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0010_auto_20140926_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
