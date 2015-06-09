#!/usr/bin/env python
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

import robot_django
import robot.process
import robot.movie
import robot.settings
import time
from threading import Thread

def search_and_create_movie_records(path,duration,fps):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            sf = os.path.splitext(filename)
            if sf[1]==".index":
                # this is based on path layout... :/
                subdir = dirpath.split("/")[-2]
                print dirpath

                # todo get subdir from path...
                robot_django.add_movie_records_from_index(duration,fps,dirpath+"/"+filename,subdir)

def search_and_process_videos(path,duration,fps):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            sf = os.path.splitext(filename)
            if sf[1]==".index":
                # this is based on path layout... :/
                subdir = dirpath.split("/")[-2]
                # todo get subdir from path...
                robot_django.chop_index(duration,fps,dirpath+"/"+filename,subdir)

def process_loop(instance_name):
    while True:
        robot_django.process_random_video(instance_name)
        time.sleep(20)


if len(sys.argv)<2 or sys.argv[1]=="-?" or sys.argv[1]=="--help":
    print "Welcome to the cricket tales processing robot v0.0.1"
else:
    if sys.argv[1]=="build":
        search_and_create_movie_records(robot.settings.srcdir,
                                        robot.settings.video_length,
                                        robot.settings.video_fps)
 
    if sys.argv[1]=="video-process":
        Thread(target = process_loop, args = ("thread-0", )).start()
        Thread(target = process_loop, args = ("thread-1", )).start()
        Thread(target = process_loop, args = ("thread-2", )).start()
        Thread(target = process_loop, args = ("thread-3", )).start()
        Thread(target = process_loop, args = ("thread-4", )).start()
        Thread(target = process_loop, args = ("thread-5", )).start()
    
    if sys.argv[1]=="player-activity":
        while True:
            robot_django.update_all_activity()
            time.sleep(30)

    if sys.argv[1]=="check":
        robot_django.update_video_status()
    if sys.argv[1]=="update-burrows":
        robot_django.update_burrows()
    if sys.argv[1]=="shuffle-burrows":
        robot_django.shuffle_burrows()
    if sys.argv[1]=="activity-update":
        robot_django.update_all_activity()

