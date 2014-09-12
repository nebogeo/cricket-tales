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
    movie_file = models.FileField(upload_to='media/cricket_movies')
    name = models.CharField(max_length=200)

class Event(models.Model):
    movie = models.ForeignKey(Movie)
    event_type = models.CharField(max_length=200)
    start_time = models.FloatField(default=0)
    end_time = models.FloatField(default=0)
