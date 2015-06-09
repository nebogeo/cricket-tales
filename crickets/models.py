from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    score = models.FloatField(default=0)
    num_events = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

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

class Burrow(models.Model):
    name = models.CharField(max_length=200)
    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)
    # stuff updated from periodic update.py
    num_movies = models.IntegerField(default=0)
    num_movies_ready = models.IntegerField(default=0)
    biggest_contributor = models.CharField(max_length=200, default="None yet")
    num_contributors = models.CharField(max_length=200, default=0)
    total_events = models.CharField(max_length=200, default=0)
    def __unicode__(self):
        return self.name;

class Movie(models.Model):
    cricket = models.ForeignKey(Cricket)
    burrow = models.ForeignKey(Burrow, null=True, blank=True, default = None)
    name = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField('date created')
    status = models.IntegerField(default=0)
    src_index_file = models.CharField(max_length=4096)
    start_frame = models.IntegerField(default=0)
    fps = models.FloatField(default=0)
    length_frames = models.IntegerField(default=0)
    # stuff updated from periodic update.py
    num_events = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.cricket)+" : "+str(self.name);

# optimisation one to many to avoid doing lookups on all the events
# in order to find which movies players have clicked on
# these are created automatically by robot.py
# premature optimisation
class PlayersToMovies(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)

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
