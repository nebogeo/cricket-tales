# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0015_auto_20150530_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='score',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
