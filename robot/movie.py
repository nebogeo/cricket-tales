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

import os
import exicatcher
import datetime
import process
import settings

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
