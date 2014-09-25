#####################################################################


import json
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from crickets.models import *
from django.core import serializers
from django.template import Context, loader, RequestContext
from itertools import chain

# todo move forms
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from django import forms

from django.contrib.auth import authenticate, login, logout

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

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['hiscores_list']=UserProfile.objects.order_by('-num_events')[:20]
        return context

######################################################################
## cricket page

class CricketView(generic.DetailView):
    model = Cricket
    template_name = 'crickets/cricket.html'

    def get_context_data(self, **kwargs):
        context = super(CricketView, self).get_context_data(**kwargs)
        context['movies']=Movie.objects.filter(cricket=context['cricket'])
        context['num_events']=len(Event.objects.filter(movie__cricket=context['cricket']))
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
            event_type.width=int(100/len(context['event_types']))*0.5

        context['events']=Event.objects.filter(movie=context['movie'])
        return context

class EventForm(ModelForm):
     class Meta:
         model = Event

## incoming from javascript...
def spit_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            # update the stats for this player
            data = form.cleaned_data
            user = User.objects.filter(id=data['user'].id)[0]
            profile = UserProfile.objects.filter(user=user)[0]
            print profile
            profile.num_tags += 1
            profile.save()

            return HttpResponse('')
        return HttpResponse('request is invalid: '+str(form))
    else:
        form = EventForm()
        return render(request, 'crickets/event.html', {'form': form})

######################################################################
## user stuff

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'crickets/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def logmein(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('crickets/login.html', {}, context)



def logmeout(request):
    logout(request)
    return HttpResponseRedirect('/')

######################################################################
## json data

def suck(request):
    data = serializers.serialize("json", Cricket.objects.all())
    return HttpResponse(json.dumps(data), content_type="application/json")

def spit(request):
    pass
