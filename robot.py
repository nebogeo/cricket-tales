#!/usr/bin/env python
# a movie creating robot for crickets

import os,sys
import exicatcher
import datetime
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales.settings")
import django
from crickets.models import *
from django.utils import timezone
import subprocess
import random

srcdir = "/synology/nas1/Storage/2013/"
dest_root = "media/movies/"

# palm:oil:chaos

django.setup()

def update_burrow_django(movie):
    burrowname = movie.name.split("/")[0]
    try:
        existing = Burrow.objects.get(name=burrowname)
    except Burrow.DoesNotExist:
        print("adding burrow: "+burrowname)
        existing = Burrow(name = burrowname, pos_x=0, pos_y=0)
        existing.save()
    if movie.burrow!=existing:
        #print("registering movie: "+movie.name+" with "+burrowname)
        movie.burrow=existing
        movie.save()

def add_movie_django(cricketname,moviename):
    # exit if it exists already
    existing = Movie.objects.filter(name=moviename)
    if len(existing)!=0: 
        print("not adding, found "+moviename)
        return

    crickets = Cricket.objects.filter(name=cricketname) 
    if len(crickets)>0:
        print("adding "+moviename)
        m = Movie(cricket = crickets[0], 
                  name = moviename,
                  created_date = timezone.now(),
                  status = 0)
        m.save()
        # find and connect, or make new burrow here
        update_burrow_django(m)
    else:
        print("add movie error, could not find cricket:"+cricketname)

def set_movie_status_django(moviename,status):
    try:
        existing = Movie.objects.get(name=moviename)
        existing.status = status
        existing.save()
        return True
    except Movie.DoesNotExist:
        return False

def get_movie_status_django(moviename):
    try:
        existing = Movie.objects.get(name=moviename)
        return existing.status
    except Movie.DoesNotExist:
        return -1
    
def examine_index(path):
    frames = exicatcher.read_index(path)
    last = ""
    f = open(path+".freq","w")
    for i,frame in enumerate(frames):
        t = frame["time"]
        dt = datetime.datetime(t[0],t[1],t[3],t[4],t[5],t[6],t[7])
        tot = 0
        if i!=0:
            delta = dt-last
            secs = delta.total_seconds()
            tot+=secs
            f.write(str(secs)+"\n")

        last = dt         
    tot/=len(frames)
    f.close()

def run(cmd):
    #print(cmd)
    os.system(cmd)

def run_converter(f,r):
    f = dest_root+f
    cmd = "avconv -y -loglevel error -r "+str(r)+" -i frames/frame-%05d.jpg -vf vflip"
    run(cmd+" -c:v libx264 "+f+".mp4")
    time.sleep(20)
    run(cmd+" "+f+".ogg")
    time.sleep(20)
    run(cmd+" "+f+".webm")
    time.sleep(20)
 
def delete_frames():
    run("rm frames/*.jpg")

def renamer(start,frames):
    if start>0:
        for i in range(0,frames):
            run("mv frames/frame-%05d.jpg frames/frame-%05d.jpg"%(i+start,i))

def create_thumb(fn):
    run("convert frames/frame-00000.jpg -resize '233x175^' -gravity center -crop '175x175+0+0' "+dest_root+fn+".jpg")

def check_done(fn):
    return (os.path.isfile(dest_root+fn+".jpg") and
            os.path.isfile(dest_root+fn+".mp4") and
            os.path.isfile(dest_root+fn+".ogg") and
            os.path.isfile(dest_root+fn+".webm"))

# don't process, just add django records with state set to 0
def add_django_record(path,subdir,start,frames,fps):
    sf = os.path.splitext(path)
    moviename = sf[0]+".generic.sfs"
    so = os.path.splitext(os.path.basename(path))
    outname = subdir+"/"+so[0]+"-"+str(start)
    add_movie_django("Unknown",outname)

# calculate frames and actually do the work, set movie state
def make_video(path,subdir,start,frames,fps):
    sf = os.path.splitext(path)
    moviename = sf[0]+".generic.sfs"
    so = os.path.splitext(os.path.basename(path))
    outname = subdir+"/"+so[0]+"-"+str(start)
    # check django record exists
    status = get_movie_status_django(outname)
    if status==-1:
        print("Error: no django record found for movie: "+outname)
        return

    # trust the status, so will overwrite existing files
    if status==0:        
        #print("extracting "+moviename+" starting "+str(start))
        exicatcher.extract(moviename, frames, "frames/frame", False)
        renamer(start,len(frames))
        #print(outname)
        create_thumb(outname)
        run_converter(outname,fps)
        delete_frames()
        set_movie_status_django(outname,1)        
    else:
        #print(outname+": status is 1 - is already done...?")
        # status is 1 so check files actually exist..
        if not check_done(outname):
            print("status is 1 but no files, setting status to 0, will get next time")
            set_movie_status_django(outname,0)        

# calculate frames and generate django records
def add_django_records_from_index(duration,fps,path,subdir):
    frames = exicatcher.read_index(path)
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

        add_django_record(path,subdir,start,frames[start:end],fps)

def chop_index(duration,fps,path,subdir):
    # check subdirectory exists and create it if not
    if not os.path.exists(dest_root+subdir):
        os.makedirs(dest_root+subdir)

    frames = exicatcher.read_index(path)
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
            print("extending: "+str(end-start)+" frames")

        make_video(path,subdir,start,frames[start:end],fps)

def search_and_create_django_records(path,duration,fps):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            sf = os.path.splitext(filename)
            if sf[1]==".index":
                # this is based on path layout... :/
                subdir = dirpath.split("/")[-2]
                # todo get subdir from path...
                add_django_records_from_index(duration,fps,dirpath+"/"+filename,subdir)

def search_and_process_videos(path,duration,fps):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            sf = os.path.splitext(filename)
            if sf[1]==".index":
                # this is based on path layout... :/
                subdir = dirpath.split("/")[-2]
                # todo get subdir from path...
                chop_index(duration,fps,dirpath+"/"+filename,subdir)

def get_video_length(filename):
    cmd = "avconv -i "+filename+" 2>&1 | grep 'Duration' | awk '{print $2}' | sed s/,//"
    out = subprocess.check_output(cmd,shell=True)
    time = map(lambda s: s.strip(),out.split(":"))
    if len(time)<2: return 0
    seconds = float(time[2])
    return seconds

def check_video_lengths(fn):
    return (get_video_length(dest_root+fn+".mp4")>=30 and
            get_video_length(dest_root+fn+".ogg")>=30 and
            get_video_length(dest_root+fn+".webm")>=30)
    
def update_video_status_django():
    for movie in Movie.objects.all():
        if check_done(movie.name):
            if not check_video_lengths(movie.name):
                print("movies too short: "+movie.name)           
                # force redo
                set_movie_status_django(movie.name,0)
            elif movie.status == 0:
                print("found a movie turned off good files, turning on: "+movie.name)
                set_movie_status_django(movie.name,1)

        if not check_done(movie.name) and movie.status == 1:
            print("!!! found a movie turned ON without files, turning off: "+movie.name)
            set_movie_status_django(movie.name,0)
    
def update_burrows():
    for movie in Movie.objects.all():
        update_burrow_django(movie)

def shuffle_burrows():
    for burrow in Burrow.objects.all():
        burrow.pos_x = random.randrange(0,800)
        burrow.pos_y = random.randrange(0,800)
        burrow.save()


if len(sys.argv)<2 or sys.argv[1]=="-?" or sys.argv[1]=="--help":
    print "Welcome to the cricket tales processing robot v0.0.1"
    print "Options are: To build django records from the video files only:"
    print "cricket_robot build" 
    print "To search for and process new videos:"
    print "cricket_robot process"
    print "To check for and amend videos turned on that don't exist or videos turned off that do:"
    print "cricket_robot check"
else:
    if sys.argv[1]=="build":        
        search_and_create_django_records(srcdir,30,3)
    if sys.argv[1]=="process":
        search_and_process_videos(srcdir,30,3)
    if sys.argv[1]=="check":
        update_video_status_django()
    if sys.argv[1]=="debug":
        get_video_length(sys.argv[2])
    if sys.argv[1]=="update-burrows":        
        update_burrows()
    if sys.argv[1]=="shuffle-burrows":        
        shuffle_burrows()









