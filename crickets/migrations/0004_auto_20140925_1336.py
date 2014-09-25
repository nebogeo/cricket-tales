# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0003_userprofile_num_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cricket',
            old_name='cricket_name',
            new_name='name',
        ),
    ]
