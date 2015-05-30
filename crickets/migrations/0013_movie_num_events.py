# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0012_auto_20150529_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='num_events',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
