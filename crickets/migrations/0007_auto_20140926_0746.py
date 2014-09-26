# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crickets', '0006_remove_userprofile_num_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='movie_file_mp4',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='movie_file_ogg',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='movie_file_webm',
        ),
        migrations.AddField(
            model_name='movie',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
