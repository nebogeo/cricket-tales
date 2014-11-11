# a movie creating robot for crickets

import os,sys
import exicatcher
import datetime
import dbadd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cricket_tales.settings")
import django
from crickets.models import *

srcdir = "/home/dave/projects/crickets/fakedisk/"

# palm:oil:chaos

django.setup()

def add_movie_django(cricketname,moviename):
    crickets = Cricket.objects.filter(name=cricketname) 
    if len(crickets)>0:
        print("adding "+moviename)
        m = Movie(cricket = crickets[0], name = moviename)
        m.save()
    else:
        print("add movie error, could not find cricket:"+cricketname)


def examine_index(path):
    frames = exicatcher.read_index(path)
    print len(frames)    
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
    print 1/tot
    f.close()

def run(cmd):
    #print(cmd)
    os.system(cmd)

dest_root = "media/movies/"

def run_converter(f,r):
    f = dest_root+f
    cmd = "avconv -y -loglevel error -i frames/frame-%05d.jpg -vf vflip -r "+str(r)
    print("making mp4")
    run(cmd+" -c:v libx264 "+f+".mp4")
    print("making ogg")
    run(cmd+" "+f+".ogg")
    print("making webm")
    run(cmd+" "+f+".webm")

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
    
def chop_video(path,subdir,start,frames,fps):
    sf = os.path.splitext(path)
    moviename = sf[0]+".generic.sfs"
    so = os.path.splitext(os.path.basename(path))
    outname = subdir+"/"+so[0]+"-"+str(start)
    if not check_done(outname):
        print("extracting "+moviename+" starting "+str(start))
        exicatcher.extract(moviename, frames, "frames/frame", False)
        renamer(start,len(frames))
        print(outname)
        create_thumb(outname)
        run_converter(outname,fps)
        delete_frames()
        dbadd.add_movie_django("Fred",outname)
    else:
        print(outname+" is done...")

def chop_index(duration,fps,path,subdir):
    frames = exicatcher.read_index(path)
    num_frames = len(frames)
    seg_length = int(round(duration*fps))
    num_segs = num_frames/seg_length
    # todo - what to do with the offcuts??
    print("seg length:"+str(seg_length))
    print("num segs:"+str(num_segs))
    for segnum in range(0,num_segs):
        start = segnum*seg_length
        chop_video(path,subdir,start,frames[start:start+seg_length],fps)

def search_videos(path,duration,fps):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            sf = os.path.splitext(filename)
            if sf[1]==".index":
                # todo get subdir from path...
                chop_index(duration,fps,dirpath+"/"+filename,"IP101")
                
search_videos(srcdir,30,10)


