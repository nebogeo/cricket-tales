# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0036_auto_20160108_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='timestamp',
        ),
    ]
