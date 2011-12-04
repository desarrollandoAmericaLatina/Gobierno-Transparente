import json
from django.shortcuts import render

from parliament.models import Party
from parliament.queries import citations_by_party, absence_by_party

# Create your views here.
def index(request):
  citations = citations_by_party(2010)
  absences = absence_by_party(2010)
  presences = dict((party, citations[party] - absences.setdefault(party, 0)) for party in citations.keys())

  citations_categories = sorted(citations.keys())
  citations_data = [{ 'name': 'Asistencias', 'data': [presences[party] for party in citations_categories] }, { 'name': 'Inasistencias', 'data': [absences[party] for party in citations_categories] }]

  attendances = [{ 'name': 'faltca', 'data': [8, 22, 10, 10, 48, 50, 38, 72, 2, 456, 4] }, { 'name': 'citaciones', 'data': [62, 557, 1267, 1044, 1987, 1721, 1696, 1882, 914, 2317, 463] }, { 'name': 'pasajes', 'data': [0, 0, 14, 12, 8, 0, 40, 32, 14, 48, 4] }, { 'name': 'licencias', 'data': [4, 42, 126, 150, 285, 253, 342, 354, 164, 349, 75] }, { 'name': 'asist', 'data': [46, 525, 1251, 1022, 1923, 1645, 1644, 1782, 908, 1843, 459] }]

  return render(request, 'index.html', {
    'citations_categories': json.dumps(citations_categories),
    'citations_data': json.dumps(citations_data),
    'attendance_data': json.dumps(attendances),
  })

