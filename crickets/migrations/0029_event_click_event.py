# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0028_auto_20151204_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='click_event',
            field=models.BooleanField(default=True),
        ),
    ]
