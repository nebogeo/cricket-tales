# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0030_auto_20151204_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
