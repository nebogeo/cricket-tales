# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0004_auto_20140925_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='num_tags',
            new_name='num_events',
        ),
    ]
