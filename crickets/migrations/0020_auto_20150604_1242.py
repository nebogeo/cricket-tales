# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0019_auto_20150604_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='length_frames',
            field=models.IntegerField(default=0),
        ),
    ]
