# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0024_auto_20150616_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='cricket',
            name='num_videos',
            field=models.IntegerField(default=0),
        ),
    ]
