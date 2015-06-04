# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0018_burrow_num_movies_ready'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='fps',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='length_frames',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='src_index_file',
            field=models.CharField(default='', max_length=4096),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='start_frame',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
