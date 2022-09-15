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

import gettext
from gettext import ngettext
import locale 

import os
import sys
from operator import attrgetter

from odf.opendocument import OpenDocumentText, load
from odf.table import Table, TableRow, TableCell
from odf import text

from .report_base import ReportBase
from reportlab.lib.units import mm
from .files import get_file_content
from .clubes import clubes


language = 'gl'
if not language:
    language = 'en'
# locale.getlocale()[0][0:2]
filename = "locale/messages_{}.mo".format(language)

try:
    trans = gettext.GNUTranslations(open(filename, "rb"))
except IOError:
    trans = gettext.NullTranslations()

trans.install() 


events = (
    "Cto. Galego de Augas Abertas",
    "Travesía Costa Oleiros",
    "Travesía Praia de Oza",
    "Travesía ao Dique",
    "Travesía Minius",
    "Travesía Ría de Vigo",
    "Travesía Sisargas Malpica",
    "Travesía Praia de Coroso",
    "Travesía Illa de Bensa",
    "Travesía Vila do Tea",
    "Etapa Final",
)

count_events = len(events)
# Puntuations
pun_tra = (30, 25, 21, 18, 16, 15, 14, 13, 12,
            11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
pun_cto = (42, 35, 29, 24, 20, 17, 15, 14, 13,
            12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2)


class Result():

    def __init__(self, event_id, pos):
        self.event_id = event_id
        self.pos = pos
        if event_id == 10:  # OLLO! o valor de event_id é un menos que o número da travesia
            if pos >= len(pun_cto):
                points = 0
            else:
                points = pun_cto[pos]
        else:
            if pos >= len(pun_tra):
                points = 0
            else:
                points = pun_tra[pos]
        self.points = points

    @property
    def name(self):
        return events[self.pos]


class Person():
    def __init__(self, person_id, full_name, gender_id, category_id, club_id):
        self.person_id = person_id
        self.name = full_name.split(',')[1].strip()
        self.surname = full_name.split(',')[0].strip()

        self.gender_id = gender_id
        self.category_id = category_id
        self.club_id = club_id
        self.results = {}

    def add_result(self, event_id, pos):
        self.results[event_id] = Result(event_id, pos)
    
    @property
    def club_name(self):
        club_name = ''
        if self.club_id in clubes:
            club_name = clubes[self.club_id][0]
        return club_name

    @property
    def results_text(self):
        values = []
        for event_id in range(count_events):
            if event_id in self.results:
                values.append(str(self.results[event_id].points))
            else:
                values.append('')
        values = '#'.join(values)
        return values

    @property
    def total_points(self):
        total = -1
        if len(self.results) > 4:
            total = 0
            results_sorted = sorted(
                self.results.values(), key=attrgetter('points'),
                reverse=True)
            for item in results_sorted[:5]:
                total += item.points
        if len(self.results) >= 8:
            total += 20
        return total

# class GrowingList(list): USADO POR VERSION marcoconti83 PODE BORRARSE
#     def __setitem__(self, index, value):
#         if index >= len(self):
#             self.extend([None]*(index + 1 - len(self)))
#         list.__setitem__(self, index, value)


class Clasaua():
    """
    Xerador de clasificacións do Circuíto Galego de Augas Abertas
    """

    def __init__(self, app_path_folder, file_path):
        """
        file_path is de csv file with clasificacions
        """
        self.app_path_folder = app_path_folder
        self.file_path = file_path
        self.persons = {}

    # def get_data_ods(self): PODE BORRARSE
    #     '''
    #     https://github.com/marcoconti83/read-ods-with-odfpy
    #     '''   
    #     self.clonespannedcolumns = True
    #     from odf.opendocument import OpenDocumentText, load
    #     from odf.table import Table, TableRow, TableCell
    #     from odf import text
    #     from odf.text import P
    #     spreadsheetdoc = load(self.file_path)

    #     sheet = spreadsheetdoc.spreadsheet        
    #     rows = sheet.getElementsByType(TableRow)
    #     arr_rows = []

    #     # for each row
    #     for row in rows:
    #         row_comment = ""
    #         arr_cells = GrowingList()
    #         cells = row.getElementsByType(TableCell)

    #         # for each cell
    #         count = 0
    #         for cell in cells:
    #             # repeated value?
    #             repeat = cell.getAttribute("numbercolumnsrepeated")
    #             if not repeat:
    #                 repeat = 1
    #                 spanned = int(cell.getAttribute('numbercolumnsspanned') or 0)
    #                 # clone spanned cells
    #                 if self.clonespannedcolumns is not None and spanned > 1:
    #                     repeat = spanned

    #             ps = cell.getElementsByType(P)
    #             text_content = ""

    #             # for each text/text:span node
    #             for p in ps:
    #                 for n in p.childNodes:
    #                     if (n.nodeType == 1 and n.tagName == "text:span"):
    #                         for c in n.childNodes:
    #                             if c.nodeType == 3:
    #                                 text_content = '{}{}'.format(
    #                                     text_content, n.data)
    #                     if n.nodeType == 3:
    #                         text_content = '{}{}'.format(text_content, n.data)

    #             if(text_content):
    #                 if(text_content[0] != "#"):  # ignore comments cells
    #                     for rr in range(int(repeat)):  # repeated?
    #                         arr_cells[count] = text_content
    #                         count += 1
    #                 else:
    #                     row_comment = row_comment + text_content + " "
    #             else:
    #                 for rr in range(int(repeat)):
    #                     count += 1

    #         # if row contained something
    #         if len(arr_cells):
    #             arr_rows.append(arr_cells)
        
    #     (EVENT_ID, POS, PERSON_ID, CLUB_ID, FULL_NAME, GENDER_ID, CATEGORY_ID) = range(7)
    #     persons = {}

    #     for values in arr_rows:
    #         event_id = int(values[EVENT_ID]) - 1
    #         pos = int(values[POS]) - 1
    #         person_id = values[PERSON_ID].strip()
    #         club_id = values[CLUB_ID].strip()
    #         if len(club_id) < 5:
    #             club_id = club_id.zfill(5)
    #         full_name = values[FULL_NAME].strip()
    #         gender_id = values[GENDER_ID].strip()
    #         category_id = values[CATEGORY_ID].strip()
    #         if person_id in persons:
    #             person = persons[person_id]
    #         else:
    #             person = Person(
    #                 person_id, full_name, gender_id, category_id, club_id)
    #             persons[person_id] = person
    #         person.add_result(event_id, pos)
    #     self.persons = persons

    def get_data_ods(self):
        '''
        Obtén os datos directamente do ODS.
        OLLO! cando unha cela está repetida o ODS márcaa como repetida e pon
        unha columna menos.
        Tamén se podería ter en conta o caso de celas xuntadas. Neste caso
        non e contempla. 
        '''

        spreadsheetdoc = load(self.file_path)

        d = spreadsheetdoc.spreadsheet
        rows = d.getElementsByType(TableRow)
        lines = []
        for row in rows:
            cells = row.getElementsByType(TableCell)

            line = []
            for cell in cells:
                repeateds = cell.getAttribute("numbercolumnsrepeated")
                if repeateds and int(repeateds) > 1:
                # cell = cell.getElementsByType(text.P)
                    for repeated in range(int(repeateds)):
                        if cell.__str__():
                            line.append(cell.__str__())
                else:
                    if cell.__str__():
                        line.append(cell.__str__())

            if len(line) == 7:
                lines.append(line)
            else:
                print("Columnas de máis.")

        (EVENT_ID, POS, PERSON_ID, CLUB_ID, FULL_NAME, GENDER_ID,
         CATEGORY_ID) = range(7)
        persons = {}

        for values in lines:
            event_id = int(values[EVENT_ID]) - 1
            pos = int(values[POS]) - 1
            person_id = values[PERSON_ID].strip()
            club_id = values[CLUB_ID].strip()
            if len(club_id) < 5:
                club_id = club_id.zfill(5)
            full_name = values[FULL_NAME].strip()
            gender_id = values[GENDER_ID].strip()
            category_id = values[CATEGORY_ID].strip()
            if person_id in persons:
                person = persons[person_id]
            else:
                person = Person(
                    person_id, full_name, gender_id, category_id, club_id)
                persons[person_id] = person
            person.add_result(event_id, pos)
        self.persons = persons

    def get_data_csv(self):
        '''
        Usado na versión inicial
        '''
        content = get_file_content(file_path=self.file_path,
                                   mode="lines",
                                   compressed=False,
                                   encoding="utf8")

        (EVENT_ID, POS, PERSON_ID, CLUB_ID, FULL_NAME, GENDER_ID,
         CATEGORY_ID) = range(7)
        persons = {}

        for line in content:
            values = line.strip().split('#')
            event_id = int(values[EVENT_ID]) - 1
            pos = int(values[POS]) - 1
            person_id = values[PERSON_ID]
            club_id = values[CLUB_ID]
            if len(club_id) < 5:
                club_id = club_id.zfill(5)
            full_name = values[FULL_NAME]
            gender_id = values[GENDER_ID]
            category_id = values[CATEGORY_ID]
            if person_id in persons:
                person = persons[person_id]
            else:
                person = Person(
                    person_id, full_name, gender_id, category_id, club_id)
                persons[person_id] = person
            person.add_result(event_id, pos)
        self.persons = persons

    def gen_person_report(self):

        persons_list = self.persons.values()
        persons_sorted = sorted(
            persons_list, key=attrgetter('surname', 'name'),
            reverse=False)
        persons_sorted = sorted(
            persons_sorted, key=attrgetter('total_points'), reverse=True)

        persons_sorted = sorted(
            persons_sorted, key=attrgetter('category_id', 'gender_id'),
            reverse=False)

        # for item in persons_sorted:
        #     line = '{} {} {} {} {}, {} {} {}'.format(
        #         item.category_id, item.gender_id, item.total_points,
        #         item.person_id, item.surname, item.name, item.club_name,
        #         item.results_text)

        file_path = os.path.join(self.app_path_folder, 'clas_depor.pdf')
        d = ReportBase(
            app_path_folder=self.app_path_folder,
            file_path=file_path,
                       orientation='portrait',
                       title="Circuíto Galego de Augas Abertas",
                       subtitle='Tempada 2021/22')

        d.insert_paragraph(
            "<b>Clasificacións individuais por categoría</b>", "CENTER")
        d.insert_spacer(1, 12)
        # cabeceira = (
        #     'Pos', 'Licenza', 'Apelidos', 'Nome', 'Clube', '1', '2', '3', '4',
        #     '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', 'Tot.')
        cabeceira = (
            'Pos', 'Licenza', 'Apelidos', 'Nome', 'Clube', '1', '2', '3', '4',
            '5', '6', '7', '8', '9', '10', '11', 'Tot.')
        num_events = 11
        table = []
        lines_title = []
        category_id = None
        gender_id = None
        num_line = 0
        pos = 1
        pos_equated = 0
        last_points = 0
        for item in persons_sorted:

            if item.category_id != category_id or item.gender_id != gender_id:
                gender = {'F': 'Feminina', 'M': 'Masculina'}
                line = [('Categoría {} {}'.format(item.category_id,
                                                  gender[item.gender_id]))]
                lines_title.append(num_line)
                table.append(line)
                table.append(cabeceira)
                category_id = item.category_id
                gender_id = item.gender_id
                num_line += 2
                pos = 0
                last_points = 0
                pos_equated = 0
            if item.total_points != -1:
                total_points = item.total_points
                if last_points:
                    if last_points == item.total_points:
                        pos_line = str(pos)
                        pos_equated += 1
                    else:
                        pos += pos_equated
                        pos_equated = 0
                        pos += 1
                        pos_line = str(pos)
                        last_points = item.total_points
                else:
                    pos += pos_equated
                    pos_equated = 0
                    pos += 1
                    pos_line = str(pos)
                    last_points = item.total_points
            else:
                pos_line = ''
                last_points = -1
                total_points = ''

            line = [pos_line, item.person_id, item.surname,
                    item.name, item.club_name]
            sep_events = item.results_text.split('#')
            line.extend(sep_events)
            line.extend([total_points])
            table.append(line)
            num_line += 1

        style = [
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN',(2, 0),(3, -1), 'LEFT'),
            # ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ('TOPPADDING', (0,0), (-1, -1), 3),
            # ('LEFTPADDING', (0,0), (-1,-1), 8),
            # ('RIGHTPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
            ]
        for i in lines_title:
            # style.append(('ALIGN',(0,i),(-1,-1), 'LEFT'))
            style.append(('FONT', (0, i), (-1, i), 'Open Sans Bold'))
            style.append(('SPAN', (0, i), (-1, i)))  # clube
            style.append(('FONT', (0, i+1), (-1, i+1), 'Open Sans Bold'))
            # style.append(('SPAN', (0, i+1), (-1, i+1)))  # clube

        col_widths = ['3%', '7%', '20%', '12%', '11%']

        col_widths.extend(['{}%'.format((42/num_events)),] * num_events)
        col_widths.extend(['5%',])
        # row_heghts = [14*mm]
        row_heghts = None
        d.insert_table(table=table, colWidths=col_widths,
                       rowHeights=row_heghts,
                       style=style, pagebreak=False)

        d.insert_spacer(1, 24)
        table = []
        table.append(('Relación de sedes:', ))
        total_items = len(events)
        corte = total_items//3
        if total_items % 3:
            corte += 1
        for i in range(corte):
            line = []
            if i < total_items:
                line.append('{}. {}'.format(i+1, events[i]))
            if (i + corte) < total_items:
                line.append('{}. {}'.format(i+corte+1, events[i+corte]))
            else:
                line.append('')
            if (i + (corte*2)) < total_items:
                line.append('{}. {}'.format(i+(corte*2)+1, events[i+(corte*2)]))
            else:
                line.append('')


            table.append(line)
        style = [
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]

        col_widths = ['33%', '33%', '34%']
        # row_heghts = [4*mm]*15
        row_heghts = None
        table = d.formata_taboa(table, font_size=7)
        d.insert_table(table=table, colWidths=col_widths,
                       rowHeights=row_heghts,
                       style=style, pagebreak=False)

        d.build_file()

    def gen_club_report(self):
        punt_by_club = 2  # Number of participants by category by club
        puntuations = []
        persons_list = self.persons.values()
        for license_id, person in self.persons.items():
            for event_id, event in person.results.items():
                puntuations.append((
                    license_id, person.club_id, person.gender_id,
                    person.category_id, event_id, event.points))

        (LICENSE, CLUB, GENDER, CATEGORY, EVENT, POINTS) = range(6)
        puntuations = sorted(
            puntuations,
            key=lambda puntuation: puntuation[POINTS],
            reverse=True)
        puntuations = sorted(
            puntuations,
            key=lambda puntuation: (
                puntuation[CLUB], puntuation[GENDER], puntuation[CATEGORY],
                puntuation[EVENT]),
            reverse=False)
        count_club = 0
        current_club = None
        clas_fem_depor = {}
        clas_mas_depor = {}
        clas_fem_maste = {}
        clas_mas_maste = {}
        # Converte as puntuacións de diccionario a táboa
        count_club = 0
        current_club = None
        (LICENSE, CLUB, GENDER, CATEGORY, EVENT, POINTS) = range(6)
        for i in puntuations:
            club = '{}.{}.{}.{}'.format(
                i[CATEGORY], i[GENDER], i[EVENT], i[CLUB])
            if current_club != club:
                current_club = '{}.{}.{}.{}'.format(
                    i[CATEGORY], i[GENDER], i[EVENT], i[CLUB])
                count_club = 0

            if count_club < punt_by_club:
                if i[GENDER] == 'F':
                    if i[CATEGORY] == 'ABSO':
                        if not i[CLUB] in clas_fem_depor:
                            clas_fem_depor[i[CLUB]] = 0
                        clas_fem_depor[i[CLUB]] += i[POINTS]
                    else:
                        if not i[CLUB] in clas_fem_maste:
                            clas_fem_maste[i[CLUB]] = 0
                        clas_fem_maste[i[CLUB]] += i[POINTS]
                elif i[GENDER] == 'M':
                    if i[CATEGORY] == 'ABSO':
                        if not i[CLUB] in clas_mas_depor:
                            clas_mas_depor[i[CLUB]] = 0
                        clas_mas_depor[i[CLUB]] += i[POINTS]
                    else:
                        if not i[CLUB] in clas_mas_maste:
                            clas_mas_maste[i[CLUB]] = 0
                        clas_mas_maste[i[CLUB]] += i[POINTS]
                count_club += 1

        # convert to tuple
        clas_fem_depor = [ (k, v) for k, v  in clas_fem_depor.items()]
        clas_mas_depor = [ (k, v) for k, v  in clas_mas_depor.items()]
        clas_fem_maste = [ (k, v) for k, v  in clas_fem_maste.items()]
        clas_mas_maste = [ (k, v) for k, v  in clas_mas_maste.items()]
        # sort
        clas_fem_depor = sorted(clas_fem_depor, key=lambda tup: tup[1],
                                reverse=True)
        clas_mas_depor = sorted(clas_mas_depor, key=lambda tup: tup[1],
                                reverse=True)
        clas_fem_maste = sorted(clas_fem_maste, key=lambda tup: tup[1],
                                reverse=True)
        clas_mas_maste = sorted(clas_mas_maste, key=lambda tup: tup[1],
                                reverse=True)

        file_path = os.path.join(self.app_path_folder, 'clas_clube.pdf')

        d = ReportBase(app_path_folder=self.app_path_folder,
                       file_path=file_path,
                       orientation='portrait',
                       title="Circuíto Galego de Augas Abertas",
                       subtitle='Tempada 2021/22')
        d.insert_spacer(1, 12)

        clasifications = (
            ('Clasificación por clubes deportistas feminina', clas_fem_depor),
            ('Clasificación por clubes deportistas masculina', clas_mas_depor),
            ('Clasificación por clubes máster feminina', clas_fem_maste),
            ('Clasificación por clubes máster masculina', clas_mas_maste),
        )
        for clasification in clasifications:
            title = clasification[0]
            res = clasification[1]
            # d.insert_paragraph("<b>{}</b>".format(title), "LEFT")
            d.insert_title_1("{}".format(title), 0)
            d.insert_spacer(1, 10)
            table = []
            current_points = None
            current_pos = 0
            for i in res:
                club_id = i[0]
                club_name = ''
                if club_id in clubes:
                    club_name = clubes[club_id][1]
                points = i[1]
                if current_points != points:
                    current_pos += 1
                    current_points = points
                    position = current_pos
                else:
                    position = ''

                line = (position, club_name, points, '')
                table.append(line)

            col_widths = ['5%', '40%', '15%', '30%']
            # col_widths = ['3%', '10%', '7%', '13%', '10%','67%']
            # row_heghts = [14*mm]
            row_heghts = None

            style = [
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('ALIGN',(2, 0),(2, -1), 'RIGHT'),
                        ('TOPPADDING', (0,0), (-1, -1), 3),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
                    ]
            d.insert_table(
                table=table,
                colWidths=col_widths,
                rowHeights=row_heghts,
                style=style,
                pagebreak=False,
                alignment='CENTER',
                )
            d.insert_spacer(1, 30)


        d.build_file()

