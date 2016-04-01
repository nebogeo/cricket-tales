# Cricket Tales Movie Robot
# Copyright (C) 2015 Dave Griffiths
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales.settings")
import django
import datetime
from crickets.models import *
from crickets.common import *
from django.utils import timezone
from django.db.models import Max, Count, Sum
from django.utils.translation import ugettext_lazy as _
import subprocess
import random
from threading import Thread

import robot.process
import robot.exicatcher
import robot.settings
import robot.maths
import robot.import_data

django.setup()

#######################################################################
# a note on movie status flag:
#
# 0 : created from index files - no videos processed yet
# 1 : video processed and active
# 2 : video has been viewed by min_complete_views people (contains this
#     many 'cricket_end's) but the files still exist
# 3 : files have been deleted
#
#######################################################################

# controls the video file recycling, see above
min_complete_views = 3

#########################################################################
# adding movies and updating burrows

def add_cricket(name,gender,born,born_at_burrow,mass_at_birth):
    # exit if it exists already
    existing = Cricket.objects.filter(name=name)
    if len(existing)!=0:
        print("not adding, found "+name)
        return

    print("adding "+name)
    m = Cricket(name = name,
                created_date = timezone.now(),
                image = "cricket_images/2X.png",
                gender = gender,
                born = born,
                born_at_burrow = born_at_burrow,
                mass_at_birth = mass_at_birth)
    m.save()

# build all the burrows from the csv file
def build_burrows(filename):
    cameras_to_burrows = robot.import_data.import_cameras_to_burrows(filename)

    # first loop over all cameras to burrows and add all the burrows
    # we'll need
    for c2b in cameras_to_burrows:
        try:
            existing = Burrow.objects.get(name=c2b["burrow"])
        except Burrow.DoesNotExist:
            print("adding burrow: "+c2b["burrow"])
            existing = Burrow(name = c2b["burrow"], pos_x=0, pos_y=0)
            existing.save()

def random_burrows(count):
    for i in range(0,count):
        Burrow(name = "rand-"+str(i), pos_x=0, pos_y=0).save()


# use the csv file to connect the movies with the right burrows
def connect_burrows_to_movies(filename):
    cameras_to_burrows = robot.import_data.import_cameras_to_burrows(filename)
    # update the movies with the right burrow id
    # loop over all movies, find the right burrow from camera and time
    for movie in Movie.objects.all():
        camera_name = movie.name[2:movie.name.find("/")]
        burrow_name = robot.import_data.get_burrow(cameras_to_burrows,camera_name,
                                                   movie.start_time.replace(tzinfo=None),
                                                   movie.end_time.replace(tzinfo=None))
        if not burrow_name:
            print("no burrow found for "+camera_name)
            print(movie.start_time)
            print(movie.end_time)
        else:
            print("connecting movie to "+burrow_name)
            burrow = Burrow.objects.get(name=burrow_name)
            movie.burrow=burrow
            movie.save()

# convert time from exicatcher to datetime format
def conv_time(t):
    return datetime.datetime(t[0],t[1],t[3],t[4],t[5],t[6],t[7]/1000)

def add_movie(cricketname,moviename,index_filename,start_frame,fps,num_frames,start_time,end_time):
    # exit if it exists already
    existing = Movie.objects.filter(name=moviename)
    if len(existing)!=0:
        print("not adding, found "+moviename)
        return

    crickets = Cricket.objects.filter(name=cricketname)
    if len(crickets)>0:
        print("adding "+moviename)

        if end_time[0]==0:
            print end_time
            print start_time
            print("time error!")
            end_time=start_time

        if start_time[0]==0:
            print("time error!")
            print end_time
            print start_time
            start_time=end_time


        m = Movie(cricket = crickets[0],
                  name = moviename,
                  created_date = timezone.now(),
                  status = 0,
                  src_index_file = index_filename,
                  start_frame = start_frame,
                  fps = fps,
                  length_frames = num_frames,
                  start_time = conv_time(start_time),
                  end_time = conv_time(end_time))
        m.save()
        # find and connect, or make new burrow here
        #update_burrow_with_movie(m)
        # now connects via cameras -> burrows, but need something replacing it here...
    else:
        print("add movie error, could not find cricket:"+cricketname)

def set_movie_status(moviename,status):
    try:
        existing = Movie.objects.get(name=moviename)
        existing.status = status
        existing.save()
        return True
    except Movie.DoesNotExist:
        return False

def get_movie_status(moviename):
    try:
        existing = Movie.objects.get(name=moviename)
        return existing.status
    except Movie.DoesNotExist:
        return -1

# don't process, just add django records with state set to 0
def add_movie_record(path,subdir,start,frames,fps):
    sf = os.path.splitext(path)
    moviename = sf[0]+".generic.sfs"
    so = os.path.splitext(os.path.basename(path))
    outname = subdir+"/"+so[0]+"-"+str(start)
    add_movie("Unknown",outname,path,start,fps,len(frames),
              frames[0]["time"], frames[len(frames)-1]["time"])

# calculate frames and generate django records
def add_movie_records_from_index(duration,fps,path,subdir):
    frames = robot.exicatcher.read_index(path)
    num_frames = len(frames)
    seg_length = int(round(duration*fps)) # ideal length
    num_segs = num_frames/seg_length
    #print("leftover frames:"+str(num_frames%seg_length))
    # adjust length to include all frames (if it doesn't quite match)
    #print("seg length:"+str(seg_length))
    #print("num segs:"+str(num_segs))
    for segnum in range(0,num_segs):
        start = segnum*seg_length
        end = start+seg_length
        if segnum==num_segs-1: # is this the last segment?
            # extend to end of the video
            end = num_frames
            #print("extending: "+str(end-start)+" frames")

        add_movie_record(path,subdir,start,frames[start:end],fps)

def update_video_status():
    for movie in Movie.objects.all():
        if robot.process.check_done(movie.name):
            #if not robot.process.check_video_lengths(movie.name):
            #    print("movies too short: "+movie.name)#
            #    print(robot.process.get_video_length(robot.settings.dest_root+movie.name+".mp4"))
            #    print(robot.process.get_video_length(robot.settings.dest_root+movie.name+".ogg"))
            #    print(robot.process.get_video_length(robot.settings.dest_root+movie.name+".webm"))
            #    force redo
            #    set_movie_status(movie.name,0)

            if movie.status == 0:
                print("found a movie turned off good files, turning on: "+movie.name)
                set_movie_status(movie.name,1)

        if not robot.process.check_done(movie.name) and movie.status == 1:
            print("!!! found a movie turned ON without files, turning off: "+movie.name)
            set_movie_status(movie.name,0)

        # is this movie complete?
        if movie.status<2 and movie.views>min_complete_views:
            print(movie.name+" is complete with "+str(movie.views)+" views")
            set_movie_status(movie,2)
            # spawn a video process
            #Thread(target = process_loop, args = ("thread-0", )).start()
            # delete files separately


def video_clearup():
    print("hello")
    for movie in Movie.objects.filter(status=2):
        print(movie.name)
        var = raw_input("Ok to delete "+movie.name+", status:"+str(movie.status)+" with "+str(movie.views)+" views? [y/n] ")
        if var=="y" or var=="Y":
            #print("not deleting "+movie.name)
            robot.process.delete_videos(movie.name)
            set_movie_status(movie,3)

# grab (new) thumbnails from old processed videos
# hopefully only needed temporarily
def update_video_thumbs():
    for movie in Movie.objects.filter(status=1):
        if robot.process.check_done(movie.name):
            robot.process.create_thumb_from_movie(movie.name)


def connect_cricket_to_movies(name,burrow,date_in,date_out):
    # find cricket
    try:
        cricket = Cricket.objects.get(name=name)
    except Cricket.DoesNotExist:
        return False

    m = Movie.objects.filter(burrow__name=burrow)
    if len(m)==0: print("no movies found for burrow: "+burrow)

    # loop over all movies at this burrow
    for movie in m:
        # todo - UTC/GMT/WTF?
        st = movie.start_time.replace(tzinfo=None)
        et = movie.end_time.replace(tzinfo=None)

        # calculate timing
        if date_in<et and date_out>st:
            print movie.name
            print date_in
            print movie.start_time
            print date_out
            print movie.end_time

            print "connect!"
            movie.cricket = cricket
            movie.save()

def shuffle_burrows(empties):
    poslist = []
    for burrow in Burrow.objects.all():
        print(burrow.name)
        p = robot.maths.find_new_location(random.choice(empties),poslist)
        poslist.append(p)
        # fix earlier dave lat/lon confusion
        burrow.pos_x = p[0]/2.0
        burrow.pos_y = p[1]*2.0
        burrow.save()

def process_random_video(instance_name):
    # pick a random one, also checks already processed ones
    make_video(random_one(Movie),instance_name)

def process_loop(instance_name):
    while True:
        process_random_video(instance_name)
        time.sleep(20)

#################################################################
## video process which need access to django...

# calculate frames and actually do the work, set movie state
def make_video(movie,instance_name):
    print("making "+movie.name)
    frames = robot.exicatcher.read_index(movie.src_index_file)
    frames = frames[movie.start_frame:movie.start_frame+movie.length_frames]
    moviename = os.path.splitext(movie.src_index_file)[0]+".generic.sfs"
    outname = movie.name
    camera_name = movie.name[2:movie.name.find("/")]

    # check django record exists

    # check subdirectory exists and create it if not
    if not os.path.exists(robot.settings.dest_root+camera_name):
        os.makedirs(robot.settings.dest_root+camera_name)

    # trust the status, so will overwrite existing files
    if movie.status==0:
        robot.exicatcher.extract(moviename, frames, instance_name+"/frame", False)
        robot.process.renamer(movie.start_frame,movie.length_frames,instance_name)
        robot.process.create_thumb(movie.name,instance_name)
        robot.process.run_converter(movie.name,movie.fps,instance_name)
        robot.process.delete_frames(instance_name)
        movie.status = 1
        movie.save()
    else:
        #print(outname+": status is 1 - is already done...?")
        # status is 1 so check files actually exist..
        if not robot.process.check_done(movie.name):
            print("status is 1 but no files, setting status to 0, will get next time")
            movie.status = 0
            movie.save()

#########################################################################
# updating data from player activity, expensive stuff to do every few mins

def disk_state():
    df = subprocess.Popen(["df", "-h", "/"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    return used+" used, "+available+" available, "+percent+" full"

def generate_report():
    cricket_end = EventType.objects.filter(name="Cricket End").first()
    return "it's yer daily cricket tales robot report\n"+
    "-----------------------------------------\n"+
    "\n"+
    "players: "+str(UserProfile.objects.all().count()))
    "movies watched: "+str(Event.objects.filter(type=cricket_end).distinct('movie').count()))
    "events recorded: "+str(Event.objects.all().count()))
    "\n"+
    "movie info\n"+
    "available: "+str(Movie.objects.filter(status=1).count()))
    "awaiting processing: "+str(Movie.objects.filter(status=0).count()))
    "done but needing deleting: "+str(Movie.objects.filter(status=2).count()))
    "finished: "+str(Movie.objects.filter(status=3).count()))
    "\n"+
    "top 10 players:\n"+
    for i,player in enumerate(PlayerBurrowScore.objects.values('player__username').order_by('player').annotate(total=Sum('movies_finished')).order_by('-total')[:10]):
        str(i)+" "+player['player__username']+": "+str(player['total']))
    "\n"+
    "last 10 stories:\n"+
    for i,story in enumerate(Story.objects.all().order_by('-time')[:10]):
        str(story.time).split()[0]+": "+str(story))
        #str(i)+" "+player.player.username+": "+str(player.total))
    "\n"+
    "disk state: "+disk_state())
    load = os.getloadavg()
    "server load average: "+str(load[0])+" "+str(load[1])+" "+str(load[2]))
    "(eight cpus, so only in trouble with MD if > 8)\n"+
    "\n"+
    "    __         .' '. \n"+
    "  _/__)        .   .       .\n"+
    " (8|)_}}- .      .        .\n"+
    "  `\__)    '. . ' ' .  . '\n"

def update_player_activity():
    for profile in UserProfile.objects.all():
        user=profile.user
        # slightly unwieldy, count the number of movies that have
        # cricket end events for this user
        cricket_end = EventType.objects.filter(name="Cricket End").first()
        profile.num_videos_watched = Event.objects.filter(user=user,type=cricket_end).distinct('movie').count()
        profile.num_burrows_owned = Burrow.objects.filter(owner=user).count()
        profile.num_events = Event.objects.filter(user=user).count()
        profile.save()

def update_burrows_activity():
    for burrow in Burrow.objects.all():
        # update the houses stuff
        hiscores = PlayerBurrowScore.objects.filter(burrow=burrow).order_by('-movies_finished')
        if len(hiscores)>0:
            hiscore=hiscores[0]
            # only award burrows after 10 movies have been watched
            # hiscore.movies_finished>10 and
            # (controversial)
            if burrow.owner != hiscore.player:
                #print("burrow "+burrow.name+" has just been owned by "+hiscore.player.username)
                burrow.new_house_needed = 1
                burrow.owner = hiscore.player
                burrow.save()

        burrow.total_events = Event.objects.filter(movie__burrow=burrow).count()
        burrow.total_contributors = PlayerBurrowScore.objects.filter(burrow=burrow).distinct('player').count()

        # slightly unwieldy, count the number of movies that have
        # cricket end events for this burrow
        cricket_end = EventType.objects.filter(name="Cricket End").first()
        burrow.num_movies_watched = Event.objects.filter(movie__burrow=burrow,type=cricket_end).distinct('movie').count()
        burrow.num_movies_unwatched = burrow.num_movies-burrow.num_movies_watched
        burrow.num_movies_ready = Movie.objects.filter(burrow=burrow,status=1).count()
        #print("total events: "+str(cricket.total_events))
        burrow.save()


def update_movies_activity():
    cricket_end = EventType.objects.filter(name="Cricket End").first()
    for movie in Movie.objects.filter(status=1):
        num_views = Event.objects.filter(type=cricket_end,movie=movie).count()
        if movie.views != num_views:
            movie.views = num_views
            movie.save()

# update the list of movies a player has created an event in
# premature optimisation
#def update_player_to_movies():
#    for user in User.objects.all():
#        for movie in Event.objects.filter(user=user).values("movie").distinct():
#            try:
#                existing = PlayersToMovies.objects.get(user=user,movie=movie)
#            except Burrow.DoesNotExist:
#                print("Player to movie added for "+user.username)
#                PlayersToMovies(user=user, movie=movie).save()

def update_all_activity():
    update_burrows_activity()
    update_player_activity()

def update_movies():
    update_movies_activity()

def test_random_movie():
    print random_burrow_one_check_status(Movie,1,1)
