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

import csv
import datetime

def import_crickets(filename, make_fn):
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                print row
                name = row[0]
                gender = row[1]
                born = row[2]
                born_at_burrow = row[3]
                mass_at_birth = row[4]
                if born == 'Unknown':
                    born = None
                else:
                    born = datetime.datetime.strptime(born,"%d-%b-%Y")

                make_fn(name,gender,born,born_at_burrow,mass_at_birth)


def connect_cricket_to_movies(filename, connect_fn):
    with open(filename) as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,row in enumerate(r):
            if i>0:
                id = row[0]
                name = row[1]
                day = row[2]
                burrow = row[3]
                date_in = row[4]
                date_out = row[5]
                date_in = datetime.datetime.strptime(date_in,"%d-%b-%Y  %H:%M")
                date_out = datetime.datetime.strptime(date_out,"%d-%b-%Y  %H:%M")

                connect_fn(name,burrow,date_in,date_out)
