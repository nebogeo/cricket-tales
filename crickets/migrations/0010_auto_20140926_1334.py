# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0009_remove_movie_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='cricket',
            name='biggest_fan',
            field=models.CharField(default=b'None yet', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cricket',
            name='num_contributors',
            field=models.CharField(default=0, max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cricket',
            name='total_events',
            field=models.CharField(default=0, max_length=200),
            preserve_default=True,
        ),
    ]
