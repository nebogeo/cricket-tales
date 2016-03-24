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
from django.db.models import Count, Sum
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
## player's map page

def map(request):
    if request.user.is_authenticated():
        context = {}
        context['user']=request.user
        context['houses_needed_for'] = Burrow.objects.filter(owner=request.user, new_house_needed=1)
        # redirect to the house builder...
        if len(context['houses_needed_for'])>0:
            context['page_title'] = "CRICKET HOUSE BUILDER"
            return render(request, 'crickets/builder.html', context)
        else:
            context['burrows'] = Burrow.objects.filter(num_movies_ready__gt=0)
            #context['burrows'] = Burrow.objects.all()

            for burrow in context['burrows']:
                # todo: this may be a bit heavy... perhaps cache in it's own table?
                player_score = 0
                t = PlayerBurrowScore.objects.filter(player=request.user,burrow=burrow)
                if t: player_score = t[0].movies_finished
                highest_score = 0
                t = PlayerBurrowScore.objects.filter(burrow=burrow).order_by('-movies_finished')
                if t: highest_score = t[0].movies_finished
                burrow.videos_to_view = highest_score - player_score

            context['num_empty_burrows'] = Burrow.objects.filter(owner__isnull=True).count()
            context['page_title'] = _("%(username)s's BURROW MAP") % {'username': request.user.username}
            context['stories'] = Story.objects.all().order_by('-time')[:3]
            context['num_players'] = User.objects.all().count()
            context['num_videos'] = Movie.objects.filter(status=1).count()

            #############################
            # todo: slow - precache??
            cricket_end = EventType.objects.filter(name="Cricket End").first()
            context['num_videos_watched'] = Event.objects.filter(type=cricket_end).distinct('movie').count()

            totals = PlayerBurrowScore.objects.values('player__username').order_by('player').annotate(total=Sum('movies_finished')).order_by('-total')
            if len(totals)>0:
                context['most_views'] = totals[0]['player__username']
            else:
                context['most_views'] = "none yet"
            #####################################

            # can we not do this on the browser??
            for story in context['stories']:
                story.text = _(story.text) % {'player': story.player}

        return render(request, 'crickets/map.html', context)

    return HttpResponseRedirect('/')

def house(request,burrow_id,house):
    context = RequestContext(request)
    burrow = Burrow.objects.filter(id=burrow_id).first()

    if request.user.is_authenticated():
        user = request.user
        # check that the details look correct

        if burrow.new_house_needed==1 and burrow.owner==user:
            burrow.house_info = house
            burrow.new_house_needed = 0
            burrow.save()
            story = Story(player=user,
                          text=_("%(player)s has built a new house."))
            story.save()

        return HttpResponseRedirect('/map/')

    return HttpResponseRedirect('/')


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

    # sort out the backgrounds (there are 8 variations and two special types)
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
        # not all videos have burrows (in anon mode)
        if burrow:
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
    return render(request, 'crickets/builder.html', context)


def update_score(user,burrow):
    # what if no burrow??
    scores = PlayerBurrowScore.objects.filter(player=user,
                                              burrow=burrow)
    if len(scores)>0:
        scores[0].movies_finished+=1
        scores[0].save()

        # make some stories out of counts of movies per user
        if scores[0].movies_finished in [10,25,50,100]:
            story = Story(player=user,
                          text=_("%(player)s has watched %(count)i movies in a burrow!") %
                         {'player':'%(player)s', # stick this back in...
                          'count':scores[0].movies_finished})
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


######################################################################
## user stuff

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeat_password')

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if not repeat_password:
            raise forms.ValidationError("You must confirm your password")
        if password != repeat_password:
            raise forms.ValidationError("Your passwords do not match")
        return repeat_password

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
            profile.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            login(request, new_user)
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    if registered:
        return HttpResponseRedirect('/map/')
    else:
        return render_to_response(
            'crickets/register.html',
            {'user_form': user_form,
             'profile_form': profile_form,
             'registered': registered,
             'page_title': _("JOIN IN AND HELP CRICKET TALES")},
            context)

def logmein(request):
    context = RequestContext(request)
    context['page_title'] = _("LOGIN TO CRICKET TALES")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/map/')
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
