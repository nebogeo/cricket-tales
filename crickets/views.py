import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from crickets.models import *

from django.core import serializers
from itertools import chain
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


class DetailView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/detail.html'

def spit(request):
    data = serializers.serialize("json", Cricket.objects.all())
    return HttpResponse(json.dumps(data), content_type="application/json")
