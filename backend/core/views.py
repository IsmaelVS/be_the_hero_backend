from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from json import dumps, loads
from core.models import Ongs, Incidents
from django.core.paginator import Paginator


@csrf_exempt
def ongs(request):
    if request.method == 'POST':
        body = loads(request.body)

        ong = Ongs(
            nome=body['nome'],
            email=body['email'],
            whatsapp=body['whatsapp'],
            cidade=body['cidade'],
            uf=body['uf']
        )
        ong.save()

        return JsonResponse({'id': ong.id}, safe=False)

    all_ongs = Ongs.objects.all()
    ongs = []
    for ong in all_ongs:
        ongs.append({
            'id': ong.id,
            'nome': ong.nome,
            'email': ong.email,
            'whatsapp': ong.whatsapp,
            'cidade': ong.cidade,
            'uf': ong.uf
        })

    return JsonResponse(ongs, safe=False)


@csrf_exempt
def incidents(request):
    if request.method == 'POST':
        data = loads(request.body)
        ong = request.headers['Authorization']

        ong = Ongs.objects.get(id=ong)

        incident = Incidents(
            title=data['title'],
            description=data['description'],
            value=data['value'],
            ong=ong
        )
        incident.save()

        return JsonResponse({'id': incident.id}, safe=False)

    all_incidents = Incidents.objects.all()
    page = request.GET['page']
    incidents = []
    for i, incident in enumerate(all_incidents):
        ong = Ongs.objects.get(id=incident.ong_id)
        incidents.append({
            'id': incident.id,
            'title': incident.title,
            'description': incident.description,
            'value': incident.value,
            'ong': incident.ong_id,
            'nome': ong.nome,
            'email': ong.email,
            'whatsapp': ong.whatsapp,
            'cidade': ong.cidade,
            'uf': ong.uf
        })

    incidents = Paginator(incidents, 5)

    return JsonResponse(incidents.page(page).object_list, safe=False)
