# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0007_auto_20140926_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cricket',
            name='image',
            field=models.ImageField(upload_to=b'cricket_images'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='thumb',
            field=models.ImageField(upload_to=b'movies'),
        ),
    ]
