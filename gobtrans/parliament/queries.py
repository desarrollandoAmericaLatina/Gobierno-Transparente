from django.db.models import F
from models import Absence, Citation, Session, Parliamentary, Senator, Deputy, \
                   Senator, Deputy, Party

def parliamentaries_by_party(party):
    senators = party.senators.all()
    return party.deputies.exclude(parliamentary__in=senators)

def citations_by_party(year):
    result = {}

    for party in Party.objects.all():
        result[party.name] = citations_for_year_by_party(year, party)

    return result


def citations_for_year_by_party(year, party):
    citations = 0
    for p in parliamentaries_by_party(party):
        citations += p.parliamentary.citations.all().count()
    return citations


def absence_by_party(year):
    result = {}

    for party in Party.objects.all():
        result[party.name] = absences_for_year_by_party(year, party)

    return result

def absences_for_year_by_party(year, party):
    absences = 0
    for p in parliamentaries_by_party(party):
        absences += Absence.objects.filter(citation__in=p.parliamentary.citations.all()).count()
    return absences
