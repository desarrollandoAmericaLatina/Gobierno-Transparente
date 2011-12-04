import json
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'index.html', {
    'citations_data': json.dumps([{ 'name': 'Asistencias', 'data': [5, 3, 4, 7], 'backgroundColor': 'green' }, { 'name': 'Inasistencias', 'data': [3, 4, 4, 2] }]),
    'attendance_data': json.dumps([{ 'name': 'faltca', 'data': [8, 22, 10, 10, 48, 50, 38, 72, 2, 456, 4] }, { 'name': 'citaciones', 'data': [62, 557, 1267, 1044, 1987, 1721, 1696, 1882, 914, 2317, 463] }, { 'name': 'pasajes', 'data': [0, 0, 14, 12, 8, 0, 40, 32, 14, 48, 4] }, { 'name': 'licencias', 'data': [4, 42, 126, 150, 285, 253, 342, 354, 164, 349, 75] }, { 'name': 'asist', 'data': [46, 525, 1251, 1022, 1923, 1645, 1644, 1782, 908, 1843, 459] }]),
    })

