# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0031_event_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
        ),
    ]
