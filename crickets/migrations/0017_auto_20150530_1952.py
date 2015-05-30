# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0016_userprofile_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='burrow',
            name='biggest_contributor',
            field=models.CharField(default=b'None yet', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='burrow',
            name='num_contributors',
            field=models.CharField(default=0, max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='burrow',
            name='num_movies',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='burrow',
            name='total_events',
            field=models.CharField(default=0, max_length=200),
            preserve_default=True,
        ),
    ]
