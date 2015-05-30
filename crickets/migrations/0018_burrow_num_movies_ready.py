# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0017_auto_20150530_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='burrow',
            name='num_movies_ready',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
