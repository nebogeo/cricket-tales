# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cricket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(verbose_name=b'date created')),
                ('image', models.ImageField(upload_to=b'cricket_images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(max_length=200)),
                ('start_time', models.FloatField(default=0)),
                ('end_time', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movie_file', models.FileField(upload_to=b'cricket_movies')),
                ('name', models.CharField(max_length=200)),
                ('cricket', models.ForeignKey(to='crickets.Cricket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_matings', models.IntegerField(default=0)),
                ('time_in_nests', models.FloatField(default=0)),
                ('cricket', models.ForeignKey(to='crickets.Cricket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='movie',
            field=models.ForeignKey(to='crickets.Movie'),
            preserve_default=True,
        ),
    ]
