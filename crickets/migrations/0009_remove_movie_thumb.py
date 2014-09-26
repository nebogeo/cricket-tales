# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0008_auto_20140926_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='thumb',
        ),
    ]
