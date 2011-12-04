# -*- coding: utf-8 -*-
import os
import sys
import itertools
import json
import sqlite3
from datetime import datetime

from gobtrans import settings
from django.core.management import setup_environ

setup_environ(settings)

from parliament.models import Parliamentary, Legislature, Senator, Deputy, \
                              Party, Substitution, Period, Session, Citation, \
                              Absence

DATA_PATH='data/'
MEMBERS_FILE='integrantes.json'
BIOS_FILE='bios.db'
PICTURES_PATH=os.path.join(DATA_PATH, 'photos')
NAME_IDS_PATH=os.path.join(DATA_PATH, 'names_ids.json')
ATTENDANCE_PATH=os.path.join(DATA_PATH, 'session_attendance.json')
TIME_FMT='%d/%m/%Y'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def usage():
    print "%s <legislature>" % sys.argv[0]

def parse_periods(periods, session_chamber, name_ids):
    for period_entry in periods:
        period, c = Period.objects.get_or_create(legislature=legislature,
                                                 from_date=datetime.strptime(period_entry[0]['fecha'], TIME_FMT),
                                                 to_date=datetime.strptime(period_entry[-1]['fecha'], TIME_FMT))

        for session_entry in period_entry:
            session, c = Session.objects.get_or_create(period=period,
                                                       chamber=session_chamber,
                                                       internal_id=int(session_entry['nro']),
                                                       date=datetime.strptime(session_entry['fecha'], TIME_FMT))

            for name in session_entry['Asisten']:
                if name not in name_ids:
                    continue
                try:
                    citation, c = Citation.objects.get_or_create(session=session, parliamentary=Parliamentary.objects.get(id_parliament=name_ids[name]))
                except Parliamentary.DoesNotExist:
                    print 'Couldnt find', name, name_ids[name], 'in the model.'
                    continue

            for name in session_entry['Faltan con']:
                if name not in name_ids:
                    continue
                try:
                    citation, c = Citation.objects.get_or_create(session=session, parliamentary=Parliamentary.objects.get(id_parliament=name_ids[name]))
                except Parliamentary.DoesNotExist:
                    print 'Couldnt find', name, name_ids[name], 'in the model.'
                    continue
                abscence, c = Absence.objects.get_or_create(citation=citation, with_notice=True)

            for name in session_entry['Faltan sin']:
                if name not in name_ids:
                    continue
                try:
                    citation, c = Citation.objects.get_or_create(session=session, parliamentary=Parliamentary.objects.get(id_parliament=name_ids[name]))
                except Parliamentary.DoesNotExist:
                    print 'Couldnt find', name, name_ids[name], 'in the model.'
                    continue
                abscence, c = Absence.objects.get_or_create(citation=citation, with_notice=False)

            #for name in session_entry['Con licencia']:
            #   if name not in name_ids:
            #       continue
            #    citation, c = Citation.objects.get_or_create(session=session, Parliamentary.objects.get(id_parliament=name_ids[name]))
            #    license, c = License.objects.get_or_create(citation=citation)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit()

    legislature, c = Legislature.objects.get_or_create(number=sys.argv[1],
                                                    from_year=1985 + 5*(int(sys.argv[1])-1),
                                                    to_year= 1985 + 5*int(sys.argv[1]))

    db = sqlite3.connect(os.path.join(DATA_PATH, BIOS_FILE))
    db.row_factory = dict_factory
    members = db.execute('SELECT * FROM datos').fetchall()

    l = []
    with open(os.path.join(DATA_PATH, MEMBERS_FILE)) as f:
        substitutes = json.load(f)
        for entry in members:
            p, c = Parliamentary.objects.get_or_create(id_parliament=entry['id'],
                                                    picture = os.path.join(PICTURES_PATH, 'Fot' + entry['id'] + '.jpg'),
                                                    first_name = entry['nombre'],
                                                    last_name = entry['apellido'])

            party, c = Party.objects.get_or_create(name=entry['partido'])


            subs_entries = filter(lambda x: x['id'] == entry['id'], substitutes)
            if len(subs_entries) == 1:
                subs_entry = subs_entries[0]

                if subs_entry['chamber'] == 'Senate':
                    chamber_member_cls = Senator
                    chamber = Substitution.SENATE
                else:
                    chamber_member_cls = Deputy
                    chamber = Substitution.DEPUTY


                chamber_member, c = chamber_member_cls.objects.get_or_create(legislature = legislature,
                                                         parliamentary = p,
                                                         party = party)
            l.append(p)
        l.sort(cmp=lambda x,y: int(x.last_name<y.last_name)*-1)

        for p in l:
            print p.last_name, p.first_name, p.id_parliament

        for entry in substitutes:
            if 'substitution_info' in entry:
                sub_from = entry['substitution_info'].get('from')
                if sub_from:
                    sub_from = datetime.strptime(sub_from[:10], TIME_FMT)
                sub_to = entry['substitution_info'].get('to')
                if sub_to:
                    sub_to = datetime.strptime(sub_to[:10], TIME_FMT)
                reason = entry['substitution_info'].get('reason')
                if reason is None:
                    reason = entry['substitution_info']['fullreason']

                p = Parliamentary.objects.get(id_parliament=entry['id'])
                if not 'substituted_id' in entry['substitution_info']:
                    print "Could not parse the following line: \"%s\"\nPlease insert the substituted parliament member: " % entry['substitution_info']['fullreason']
                    substituted = raw_input()
                else:
                    substituted = entry['substitution_info']['substituted_id']
                if substituted is not None and substituted != 'NULL' and substituted != '':
                    substituted = Parliamentary.objects.get(id_parliament=substituted)
                else:
                    substituted = None
                if entry['chamber'] == 'Senate':
                    chamber = Substitution.SENATE
                else:
                    chamber = Substitution.DEPUTY

                sub, c = Substitution.objects.get_or_create(parliamentary=p,
                                                            substitutes=substituted,
                                                            in_chamber=chamber,
                                                            from_date=sub_from,
                                                            to_date=sub_to,
                                                            reason=reason)


    # Attendance
    with open(ATTENDANCE_PATH) as att_f:
        with open(NAME_IDS_PATH) as names_f:

            attendance = json.loads(json.load(att_f))
            name_ids = json.load(names_f)

            parse_periods(attendance['senadores'], Session.SENATE, name_ids)
            parse_periods(attendance['representantes'], Session.DEPUTY, name_ids)

