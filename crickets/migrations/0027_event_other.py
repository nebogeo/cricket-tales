# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0026_auto_20151204_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='other',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
