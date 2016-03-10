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

# using avconv to make and inspect video data

import os
import time
import subprocess
import settings

def run(cmd):
    #print(cmd)
    os.system(cmd)

def run_converter(f,r,instance_name):
    f = settings.dest_root+f
    cmd = "avconv -y -loglevel error -r "+str(r)+" -i "+instance_name+"/frame-%05d.jpg -vf vflip"
    run(cmd+" -c:v libx264 -threads 1 "+f+".mp4")
    run(cmd+" "+f+".ogg")
    run(cmd+" "+f+".webm")

def delete_frames(instance_name):
    run("rm "+instance_name+"/*.jpg")

def renamer(start,frames,instance_name):
    if start>0:
        for i in range(0,frames):
            run(("mv "+instance_name+"/frame-%05d.jpg "+instance_name+"/frame-%05d.jpg")%(i+start,i))

def create_thumb(fn,instance_name):
    #run("convert "+instance_name+"/frame-00000.jpg -resize '233x175^' -gravity center -crop '175x175+0+0' "+settings.dest_root+fn+".jpg")
    # no longer any processing needed (not checked yet)
    run("cp "+instance_name+"/frame-00000.jpg "+settings.dest_root+fn+".jpg")

def create_thumb_from_movie(fn):
    run("avconv -i "+settings.dest_root+fn+".mp4 -r 1 -vframes 1 -f image2 "+settings.dest_root+fn+".jpg > /dev/null")

def check_done(fn):
    return (os.path.isfile(settings.dest_root+fn+".jpg") and
            os.path.isfile(settings.dest_root+fn+".mp4") and
            os.path.isfile(settings.dest_root+fn+".ogg") and
            os.path.isfile(settings.dest_root+fn+".webm"))

def get_video_length(filename):
    cmd = "avconv -i "+filename+" 2>&1 | grep 'Duration' | awk '{print $2}' | sed s/,//"
    out = subprocess.check_output(cmd,shell=True)
    time = map(lambda s: s.strip(),out.split(":"))
    if len(time)<2: return 0
    seconds = float(time[2])
    return seconds

def check_video_lengths(fn):
    return (get_video_length(settings.dest_root+fn+".mp4")>=settings.video_length and
            get_video_length(settings.dest_root+fn+".ogg")>=settings.video_length and
            get_video_length(settings.dest_root+fn+".webm")>=settings.video_length)
