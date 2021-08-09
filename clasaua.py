# -*- coding: utf-8 -*-


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2019 Federacion Galega de Natación (FEGAN) http://www.fegan.org
# Author: Daniel Muñiz Fontoira (2017) <dani@damufo.com>

'''
file_path is a CSV with
event_id#position#license_id#club_id#surname, name#gender_id#category_id

event_id: is a number
position: is a number, position relative to gender and category
license_id: is a license code identificator
club_id: is 5 the digits code for club
surname, name: participant surname, name 
gender_id: [M:male|F:female]
category_id: [ABSO|MASTE1|MASTER2|MASTER3|MASTER4]
'''


import os
from classes.clasaua import Clasaua


app_path_folder = os.path.dirname(os.path.realpath(__file__))
os.chdir(app_path_folder)
file_path = None
list_files = os.listdir(app_path_folder)
for i in list_files:
    if os.path.splitext(i)[1] == '.ods':
        file_path = os.path.join(app_path_folder, i)
        break

if file_path:
    clasaua = Clasaua(app_path_folder=app_path_folder,
                      file_path=file_path)
    clasaua.get_data_ods()
    clasaua.gen_person_report()
    clasaua.gen_club_report()
