# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0014_auto_20150530_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='burrow',
            field=models.ForeignKey(default=None, blank=True, to='crickets.Burrow', null=True),
            preserve_default=True,
        ),
    ]
