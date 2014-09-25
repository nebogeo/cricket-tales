# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0005_auto_20140925_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='num_events',
        ),
    ]
