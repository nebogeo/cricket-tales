# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0033_auto_20151210_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='other',
            field=models.CharField(default=None, max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='x_pos',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='y_pos',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
    ]
