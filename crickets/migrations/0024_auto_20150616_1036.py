# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0023_auto_20150615_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='end_time',
            field=models.DateTimeField(default=datetime.date(2015, 6, 16), verbose_name=b'end time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='start_time',
            field=models.DateTimeField(default=datetime.date(2015, 6, 16), verbose_name=b'start time'),
            preserve_default=False,
        ),
    ]
