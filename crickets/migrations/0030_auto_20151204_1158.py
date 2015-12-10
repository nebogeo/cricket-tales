# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0029_event_click_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='click_event',
        ),
        migrations.AddField(
            model_name='eventtype',
            name='click_event',
            field=models.BooleanField(default=True),
        ),
    ]
