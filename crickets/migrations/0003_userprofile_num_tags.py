# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0002_auto_20140925_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='num_tags',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
