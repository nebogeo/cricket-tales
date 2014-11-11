import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales.settings")

import django
from crickets.models import *

django.setup()

def add_movie_django(cricketname,moviename):
    crickets = Cricket.objects.filter(name=cricketname) 
    if len(crickets)>0:
        print("adding "+moviename)
        m = Movie(cricket = crickets[0], name = moviename)
        m.save()
    else:
        print("add movie error, could not find cricket:"+cricketname)
