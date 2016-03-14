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

# some maths for calculating random burrow positions

import math
import random

def mag(a):
    return math.sqrt(a[0]*a[0] + a[1]*a[1])

def distance(a,b):
    return mag([a[0]-b[0],a[1]-b[1]])

def random_pos(area):
    return [random.uniform(area[0],area[2]),
            random.uniform(area[1],area[3])]

def check_list(np,poslist):
    for p in poslist:
        if distance(p,np)<2:
            return False
    return True

def find_new_location(area,poslist):
    np = random_pos(area)
    found = False
    while not found:
        found = check_list(np,poslist)
        if not found: np = random_pos()
    return np

def unit_test():
    assert(mag([100,0])==100)
    assert(mag([0,0])==0)
    assert(distance([0,0],[100,0])==100)
    assert(distance([50,0],[100,0])==50)
    assert(check_list([0,10],[[5,0],[10,0]])==False)
    assert(check_list([60,0],[[5,0],[10,0]])==True)
