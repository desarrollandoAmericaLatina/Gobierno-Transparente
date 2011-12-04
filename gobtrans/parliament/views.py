# -*- coding: utf-8 -*-
import json
from django.shortcuts import render

def index(request):
  citations_categories = [
    'Frente Amplio',
    'Partido Colorado',
    'Partido Independiente',
    'Partido Nacional',
  ]
  citations_data = [
    { 'name': 'Asistencias', 'data': [8360, 2692, 256, 4501] },
    { 'name': 'Inasistencias', 'data': [326, 210, 4, 546] },
  ]

  attendances = [
    { 'name': 'Frente Amplio',
      'data': [0, 16, 24, 14, 14, 48, 2, 30, 24, 68, 33, 53] },
    { 'name': 'Partido Colorado',
      'data': [0, 2, 10, 14, 4, 38, 16, 10, 16, 32, 22, 46] },
    { 'name': 'Partido Independiente',
      'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2] },
    { 'name': 'Partido Nacional',
      'data': [0, 30, 54, 36, 33, 79, 28, 20, 24, 92, 47, 103] },
   ]

  return render(request, 'index.html', {
    'citations_categories': json.dumps(citations_categories),
    'citations_data': json.dumps(citations_data),
    'attendance_data': json.dumps(attendances),
  })

