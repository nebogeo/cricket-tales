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

# common stuff to site and robot

from django.db.models import Max
from random import randint

# fast random selection
def random_one(model):
   max_ = model.objects.aggregate(Max('id'))['id__max']
   i = 0
   while i < 1:
       try:
           return model.objects.get(pk=randint(1, max_))
           i += 1
       except model.DoesNotExist:
           pass

# fast random selection
def random_one_check_status(model, status):
   max_ = model.objects.aggregate(Max('id'))['id__max']
   while True:
      try:
         choice = model.objects.get(pk=randint(1, max_))
         if choice.status==status:
            return choice
      except model.DoesNotExist:
         pass

def random_burrow_one_check_status(model, burrow, status):
   return model.objects.filter(burrow=burrow).order_by('?').first()
