import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales.settings")

import django
from django.db.models import Count
from crickets.models import *

django.setup()

crickets = Cricket.objects.all()

for cricket in crickets:
    print("cricket:"+str(cricket))

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
