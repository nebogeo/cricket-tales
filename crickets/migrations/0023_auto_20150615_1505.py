# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0022_remove_userprofile_num_movies'),
    ]

    operations = [
        migrations.AddField(
            model_name='cricket',
            name='born',
            field=models.DateTimeField(null=True, verbose_name=b'date born', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cricket',
            name='born_at_burrow',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cricket',
            name='gender',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cricket',
            name='mass_at_birth',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
