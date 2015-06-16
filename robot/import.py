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
                make_fn(name,gender,born,born_at_burrow,mass_at_birth)
