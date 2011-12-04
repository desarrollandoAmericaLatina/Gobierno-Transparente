# -*- coding: utf-8 -*-
from django.db.models import F
from models import Absence, Citation, Session, Parliamentary, Senator, Deputy, Senator, Deputy

def citations_by_party(year):
    result = {}

    parliamentaries = Parliamentary.objects.filter(citations__session__date__year=year)

    for senator in Senator.objects.filter(parliamentary__in=parliamentaries):
        result.setdefault(senator.party.name, 0)
        result[senator.party.name] += 1

    for deputy in Deputy.objects.filter(parliamentary__in=parliamentaries):
        result.setdefault(deputy.party.name, 0)
        result[deputy.party.name] += 1

    return result


def absence_by_party(year):
    result = {}

    absences = Absence.objects.filter(citation__session__date__year=year)
    parliamentaries = Parliamentary.objects.filter(citations__absences__in=absences)

    for senator in Senator.objects.filter(parliamentary__in=parliamentaries):
        result.setdefault(senator.party.name, 0)
        result[senator.party.name] += 1

    for deputy in Deputy.objects.filter(parliamentary__in=parliamentaries):
        result.setdefault(deputy.party.name, 0)
        result[deputy.party.name] += 1

    return result

