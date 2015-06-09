# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0021_auto_20150609_1031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='num_movies',
        ),
    ]
