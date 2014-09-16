from django.db import models


class Cricket(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField('date created')
    image = models.ImageField(upload_to='media/cricket_images')
    def __unicode__(self):
        return self.name;

class Personality(models.Model):
    cricket = models.ForeignKey(Cricket)
    num_matings = models.IntegerField(default=0)
    time_in_nests = models.FloatField(default=0)

class Movie(models.Model):
    cricket = models.ForeignKey(Cricket)
    thumb =  models.ImageField(upload_to='media/cricket_thumbs')
    movie_file_webm = models.FileField(upload_to='media/cricket_movies')
    movie_file_ogg = models.FileField(upload_to='media/cricket_movies')
    movie_file_mp4 = models.FileField(upload_to='media/cricket_movies')
    def __unicode__(self):
        return str(self.movie_file_webm);

class EventType(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.name);

class Event(models.Model):
    movie = models.ForeignKey(Movie)
    type = models.ForeignKey(EventType)
    start_time = models.FloatField(default=0)
    end_time = models.FloatField(default=0)
    def __unicode__(self):
        return self.event_type+" "+str(self.start_time);
