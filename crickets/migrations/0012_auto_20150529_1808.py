# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0011_movie_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 29, 18, 8, 45, 349145, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
