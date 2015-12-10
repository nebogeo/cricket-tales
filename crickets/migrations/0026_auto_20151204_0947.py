# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0025_cricket_num_videos'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='x_pos',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='event',
            name='y_pos',
            field=models.FloatField(default=None),
        ),
    ]
