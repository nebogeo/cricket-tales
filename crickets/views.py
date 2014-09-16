#####################################################################


import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from crickets.models import *
from django.core import serializers
from django.template import Context, loader
from itertools import chain

#####################################################################
## index

class IndexView(generic.ListView):
    template_name = 'crickets/index.html'
    context_object_name = 'crickets_list'
    def get_queryset(self):

        return chain(Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
                     Cricket.objects.order_by('-created_date'),
        )

######################################################################
## cricket page

class CricketView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/cricket.html'

    def get_context_data(self, **kwargs):
        context = super(CricketView, self).get_context_data(**kwargs)
        context['movies']=Movie.objects.filter(cricket=context['cricket'])
        return context

######################################################################
## movie page

class MovieView(generic.DetailView):
    model = Movie
    template_name = 'crickets/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)

        context['event_types']=EventType.objects.all()
        for c, event_type in enumerate(context['event_types']):
            event_type.width=int(100/len(context['event_types']))

        context['events']=Event.objects.filter(movie=context['movie'])
        for event in context['events']:
            event.left=int(event.start_time*10)



        return context

######################################################################
## json data

def spit(request):
    data = serializers.serialize("json", Cricket.objects.all())
    return HttpResponse(json.dumps(data), content_type="application/json")
