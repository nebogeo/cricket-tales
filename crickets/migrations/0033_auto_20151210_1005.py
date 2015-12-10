# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0032_auto_20151204_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='other',
        ),
        migrations.RemoveField(
            model_name='event',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='event',
            name='x_pos',
        ),
        migrations.RemoveField(
            model_name='event',
            name='y_pos',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='click_event',
        ),
    ]
