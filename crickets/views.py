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
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

# todo move forms
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from django import forms

from django.contrib.auth import authenticate, login, logout


#####################################################################
## index

def index(request):
    context = {}
    context['hide_menu'] = True
    return render(request, 'crickets/index.html', context)

######################################################################
## player page

def player(request,pk):
    context = {}

    context["user"] = User.objects.filter(id=pk).first()
    context['houses_needed_for'] = Burrow.objects.filter(owner=context["user"], new_house_needed=1)
    # redirect to the house builder...
    if len(context['houses_needed_for'])>0:
        context['page_title'] = "CRICKET HOUSE BUILDER"
        return render(request, 'crickets/builder.html', context)
    else:
        context['movies'] = PlayerBurrowScore.objects.filter(player=context["user"])
        context['burrows'] = Burrow.objects.all()
        context['page_title'] = _("%(username)s's BURROW MAP") % {'username': context["user"].username}
        context['stories'] = Story.objects.all().order_by('-time')[:5]

        # can we not do this on the browser??
        for story in context['stories']:
            story.text = _(story.text) % {'player': context['user'].username}

        return render(request, 'crickets/player.html', context)


######################################################################
## movie page

def get_event_types():
    event_types = [
        EventType.objects.filter(name="MATE").first(),
        EventType.objects.filter(name="SING").first(),
        EventType.objects.filter(name="FIGHT").first(),
        EventType.objects.filter(name="FEED").first(),
        EventType.objects.filter(name="LEAVES BURROW").first(),
        EventType.objects.filter(name="ENTERS BURROW").first(),
        EventType.objects.filter(name="ANOTHER CRICKET").first(),
        EventType.objects.filter(name="LEAVES FRAME").first(),
        EventType.objects.filter(name="Predator: Bird").first(),
        EventType.objects.filter(name="Predator: Shrew").first(),
        EventType.objects.filter(name="TRAP").first()]

    for c, event_type in enumerate(event_types):
        event_type.title = True
        event_type.image = (c%7)+1 # rotate variations
        if c == 8:
            event_type.image = 8 # bird
            event_type.title = False
        if c == 9:
            event_type.image = 9 # shrew
            event_type.title = False
    return event_types

class MovieView(generic.DetailView):
    model = Movie
    template_name = 'crickets/movie.html'

    def get_context_data(self, **kwargs):
        context = super(MovieView, self).get_context_data(**kwargs)
        # inc views
        context['movie'].views+=1
        context['movie'].save()

        # When page loads, mark as 'watched', this will need to be changed to 50%
        burrow = context['movie'].burrow
        burrow.num_movies_unwatched = burrow.num_movies_ready - burrow.num_movies_watched
        burrow.save()

        # order these explicitly
        context['page_title'] = _("MOVIE")
        context['event_types']=get_event_types()
        context['something_else'] = EventType.objects.filter(name="Something Else").first()
        context['cricket_start'] = EventType.objects.filter(name="Cricket Start").first()
        context['cricket_end'] = EventType.objects.filter(name="Cricket End").first()
        context['burrow_start'] = EventType.objects.filter(name="Burrow Start").first()
        context['cricket_id'] = EventType.objects.filter(name="Cricket ID").first()
        return context

class EventForm(ModelForm):
     class Meta:
         model = Event
         fields = "__all__"

## Static house builder
def house_builder(request,id):
    context = RequestContext(request)
    print(context)
    return render(request, 'crickets/builder.html', context)


def update_score(user,burrow):
    # what if no burrow??
    scores = PlayerBurrowScore.objects.filter(player=user,
                                              burrow=burrow)
    print scores
    if len(scores)>0:
        scores[0].movies_finished+=1
        scores[0].save()

        # make some stories out of counts of movies per user
        if scores[0].movies_finished in [10,25,50,100]:
            story = Story(player=user,
                          text=_("%(player)s has now watched %(count)i burrows!") %
                         {'count':scores[0].movies_finished})
            story.save()
    else:
        score = PlayerBurrowScore(player=user,
                                  burrow=burrow,
                                  movies_finished=1)
        score.save()

def update_stories(user,data):
    # make some stories
    if data['type'].name == "Cricket ID":
        story = Story(player=user,
                      text=_("A cricket has just been IDed by %(player)s"))
        story.save()

    if data['type'].name == "Predator: Bird":
        story = Story(player=user,
                      text=_("A bird has been spotted by %(player)s"))
        story.save()

    if data['type'].name == "Predator: Shrew":
        story = Story(player=user,
                      text=_("%(player)s has seen a shrew!"))
        story.save()

    if data['type'].name == "SING":
        story = Story(player=user,
                      text=_("A cricket has been seen singing by %(player)s"))
        story.save()

    if data['type'].name == "FIGHT":
        story = Story(player=user,
                      text=_("A fight has been spotted by %(player)s"))
        story.save()


## incoming from javascript...
def spit_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            # update the stats for this player
            # too much here???
            # either this or a laggy continual robot.py process
            data = form.cleaned_data

            # if we're not anonymous
            if data["user"]:
                profile = data["user"].profile
                profile.num_events+=1
                profile.save()

                user = data["user"]
                movie = data["movie"]

                # update the score for this user if it's the last
                # event (we can also calculate these by counting the
                # cricket end's in the event table if we need to)
                if data["type"].name == "Cricket End":
                    update_score(user,movie.burrow)

                update_stories(user,data)

            return HttpResponse('')
        return HttpResponse('request is invalid: '+str(form))
    else:
        form = EventForm()
        return render(request, 'crickets/event.html', {'form': form})

## need to be a bit careful here, as these could come from anywhere
def update_house(request):
    if request.method == 'POST':
        r = request.POST
        burrow = Burrow.objects.filter(id=r['burrow']).first()
        user = User.objects.filter(id=r['user']).first()
        if burrow.new_house_needed==1 and burrow.owner==user:
            burrow.house_info = r['house']
            burrow.new_house_needed = 0
            burrow.save()
            story = Story(player=user,
                          text=_("%(player)s has built a new house."))
            story.save()

    return HttpResponse('')






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
        fields = ('age_range',)

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
                return HttpResponse(_("Your account is disabled."))
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse(_("Invalid login details supplied."))

    else:
        return render_to_response('crickets/login.html', {}, context)

def tutorial(request):
    context = {}
    context['page_title'] = _("HOW YOU CAN HELP")
    context['event_types'] = get_event_types()
    context['something_else'] = EventType.objects.filter(name="Something Else").first()
    context['cricket_start'] = EventType.objects.filter(name="Cricket Start").first()
    context['cricket_end'] = EventType.objects.filter(name="Cricket End").first()
    context['burrow_start'] = EventType.objects.filter(name="Burrow Start").first()
    context['cricket_id'] = EventType.objects.filter(name="Cricket ID").first()
    return render(request, 'crickets/tutorial.html', context)

def about(request):
    context = {}
    context['page_title'] = _("ABOUT THE PROJECT")
    return render(request, 'crickets/about.html', context)

def logmeout(request):
    logout(request)
    return HttpResponseRedirect('/')

# redirect to a random movie
def random_movie(request):
    return HttpResponseRedirect('/movie/'+str(random_one_check_status(Movie,1).pk))

# redirect to random movie of burrow
def random_burrow_movie(request, id):
    burrow = Burrow.objects.filter(id=id)
    return HttpResponseRedirect('/movie/'+str(random_burrow_one_check_status(Movie,burrow,1).pk))

######################################################################
## json data

#def suck(request):
#    data = serializers.serialize("json", Cricket.objects.all())
#    return HttpResponse(json.dumps(data), content_type="application/json")
