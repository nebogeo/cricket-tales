# Cricket Tales Movie Robot
# Copyright (C) 2015 Dave Griffiths
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.contrib.auth.models import User
from common import *
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    score = models.FloatField(default=0)
    # these 3 updated by robot
    num_events = models.IntegerField(default=0)
    num_videos_watched = models.IntegerField(default=0)
    num_burrows_owned = models.IntegerField(default=0)

    ethics_agreed = models.IntegerField(default=0)
    age_range = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Burrow(models.Model):
    name = models.CharField(max_length=200)
    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)
    # stuff updated from periodic update.py
    num_movies = models.IntegerField(default=0)
    num_movies_ready = models.IntegerField(default=0)
    num_movies_watched = models.IntegerField(default=0)
    num_movies_unwatched = models.IntegerField(default=0)
    owner = models.ForeignKey(User, null=True, blank=True, default = None)
    # (updated from update.py)
    new_house_needed = models.IntegerField(default=0)
    total_contributors = models.IntegerField(default=0)

    total_events = models.CharField(max_length=200, default=0)
    house_info = models.CharField(max_length=200, blank=True, default='')

    def __unicode__(self):
        return self.name;

class PlayerBurrowScore(models.Model):
    player = models.ForeignKey(User)
    burrow = models.ForeignKey(Burrow)
    movies_finished = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.player.username+" "+self.burrow.name)

class Story(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(User)
    text = models.CharField(max_length=1024, blank=True, default='')
    def __unicode__(self):
        return self.text % {'player':self.player.username}

class Movie(models.Model):
    burrow = models.ForeignKey(Burrow, null=True, blank=True, default = None)
    name = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField('date created')
    status = models.IntegerField(default=0)
    src_index_file = models.CharField(max_length=4096)
    start_frame = models.IntegerField(default=0)
    fps = models.FloatField(default=0)
    length_frames = models.IntegerField(default=0)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    # stuff updated from periodic update.py
    num_events = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.name);

class EventType(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.name);

class Event(models.Model):
    movie = models.ForeignKey(Movie)
    type = models.ForeignKey(EventType)
    user = models.ForeignKey(User, null=True, blank=True, default = None)
    start_time = models.FloatField(default=0)
    end_time = models.FloatField(default=0)
    x_pos = models.FloatField(null=True, blank=True, default=None)
    y_pos = models.FloatField(null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    other = models.CharField(max_length=200, null=True, blank=True, default=None)
    def __unicode__(self):
        return self.type.name+" "+str(self.start_time)+" : "+str(self.movie);
