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
import smtplib

import robot_django
import robot.process
import robot.movie
import robot.settings
import robot.import_data
import time
from threading import Thread
import map.generate

report_recipients = ["dave@fo.am"]

def send_email(f,to,subject,text):
    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (f, ", ".join(to), subject, text)
    server = smtplib.SMTP("localhost")
    server.sendmail(f, to, message)
    server.quit()

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


if len(sys.argv)<2 or sys.argv[1]=="-?" or sys.argv[1]=="--help":
    print "Welcome to the cricket tales processing robot v0.0.1"
else:
    if sys.argv[1]=="build-movies":
        search_and_create_movie_records(robot.settings.srcdir,
                                        robot.settings.video_length,
                                        robot.settings.video_fps)
    if sys.argv[1]=="build-burrows":
        robot_django.build_burrows("cricket-data/camera-burrow.csv")

    if sys.argv[1]=="build-crickets":
        #robot.import_data.import_crickets("cricket-data/crickets.csv",robot_django.add_cricket)
        robot.import_data.connect_cricket_to_movies("cricket-data/crickets-timing.csv",robot_django.connect_cricket_to_movies)

    if sys.argv[1]=="video-process":
        Thread(target = robot_django.process_loop, args = ("thread-0", )).start()
        Thread(target = robot_django.process_loop, args = ("thread-1", )).start()
        Thread(target = robot_django.process_loop, args = ("thread-2", )).start()
        Thread(target = robot_django.process_loop, args = ("thread-3", )).start()
        Thread(target = robot_django.process_loop, args = ("thread-4", )).start()
        Thread(target = robot_django.process_loop, args = ("thread-5", )).start()

    if sys.argv[1]=="player-activity":
        while True:
            robot_django.update_all_activity()
            time.sleep(1)

    if sys.argv[1]=="update-movie-burrows":
        robot_django.connect_burrows_to_movies("cricket-data/camera-burrow.csv")


    if sys.argv[1]=="check-videos":
        robot_django.update_video_status()

    if sys.argv[1]=="video-clearup":
        robot_django.video_clearup()

    if sys.argv[1]=="make-map":
        # make new map image - overrites empties and out.jpg
        image_size = 16384
        empties = map.generate.gen_square(image_size,1034,["1","2","3","4","5","7","8","9"],["t1","t1","t2","t4","t5"])
        f = open("empty-map-zones.txt","wo")
        for empty in empties:
            f.write(str(empty[0])+" "+str(empty[1])+" "+
                    str(empty[2])+" "+str(empty[3])+"\n")
        f.close()
    if sys.argv[1]=="shuffle-burrows":
        empties = []
        for l in open("empty-map-zones.txt"):
            l = l.split()
            # not sure why these divides, but fed up and works
            ret = [float(l[0])/2, float(l[1])/8,
                   float(l[2])/2, float(l[3])/8]
            empties.append(ret)

        robot_django.shuffle_burrows(empties)
    if sys.argv[1]=="random-burrows":
        robot_django.random_burrows(1000)
    if sys.argv[1]=="activity-update":
        robot_django.update_all_activity()
    if sys.argv[1]=="report":
        report = robot_django.generate_report()
        send_email("robot@cricket-tales.ex.ac.uk",
                   report_recipients,"cricket tales report",
                   report)
    if sys.argv[1]=="overwrite-thumbnails":
        robot_django.update_video_thumbs()
    if sys.argv[1]=="test":
        robot_django.test_random_movie()
