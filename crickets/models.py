from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __unicode__(self):
        return self.user.username

class Cricket(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField('date created')
    image = models.ImageField(upload_to='cricket_images')
    # stuff updated from periodic update.py
    biggest_fan = models.CharField(max_length=200, default="None yet")
    num_contributors = models.CharField(max_length=200, default=0)
    total_events = models.CharField(max_length=200, default=0)
    def __unicode__(self):
        return self.name;

class Personality(models.Model):
    cricket = models.ForeignKey(Cricket)
    num_matings = models.IntegerField(default=0)
    time_in_nests = models.FloatField(default=0)

class Movie(models.Model):
    cricket = models.ForeignKey(Cricket)
    name = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.cricket)+" : "+str(self.name);

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
    def __unicode__(self):
        return self.type.name+" "+str(self.start_time)+" : "+str(self.movie);
