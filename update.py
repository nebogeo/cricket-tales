import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales.settings")

import django
from django.db.models import Count
from crickets.models import *

django.setup()

crickets = Cricket.objects.all()

print("crickets...")

for cricket in crickets:
    #print("cricket:"+str(cricket))
    fans = Event.objects.filter(movie__cricket=cricket)\
                        .exclude(user__isnull=True)\
                        .values('user__username')\
                        .annotate(count=Count('user'))\
                        .order_by('-count')
    if len(fans)>0:
        cricket.biggest_fan=fans[0]["user__username"]
        print("biggest fan is: "+cricket.biggest_fan)
    cricket.num_contributors = len(fans)
    print("with "+str(cricket.num_contributors)+" contributors")
    cricket.total_events = Event.objects.filter(movie__cricket=cricket).count()
    print("total events: "+str(cricket.total_events))
    cricket.save()

print("burrows...")

for burrow in Burrow.objects.all():
    fans = Event.objects.filter(movie__burrow=burrow)\
                        .exclude(user__isnull=True)\
                        .values('user__username')\
                        .annotate(count=Count('user'))\
                        .order_by('-count')
    if len(fans)>0:
        burrow.biggest_contributor=fans[0]["user__username"]
    burrow.num_contributors = len(fans)
    #print("with "+str(cricket.num_contributors)+" contributors")
    burrow.total_events = Event.objects.filter(movie__burrow=burrow).count()
    burrow.num_movies = Movie.objects.filter(burrow=burrow).count()
    burrow.num_movies_ready = Movie.objects.filter(burrow=burrow,status=1).count()
    #print("total events: "+str(cricket.total_events))
    burrow.save()
    
print("movies...")

for movie in Movie.objects.all():
    num_events = Event.objects.filter(movie=movie).count()
    if movie.num_events != num_events:
        movie.num_events = num_events
        movie.save()

