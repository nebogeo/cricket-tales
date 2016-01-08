# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0042_auto_20160108_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
