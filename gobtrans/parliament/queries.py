from django.db.models import F
from models import Absence, Citation, Session, Parliamentary, Senator, Deputy, Senator, Deputy

def absence_by_party(party):
    res = []
    senate_absences = Absence.objects.filter(citation__session__chamber=Session.SENATE)
    deputy_absences = Absence.objects.filter(citation__session__chamber=Session.DEPUTY)
    for absence in senate_absences:
        for senator in Senator.objects.filter(parliamentary=absence.citation.parliamentary, party__name=party):
            res.append(absence)
    for absence in deputy_absences:
        for deputy in Deputy.objects.filter(parliamentary=absence.citation.parliamentary, party__name=party):
            res.append(absence)

    return res
