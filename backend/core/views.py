from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer
from json import dumps, loads
from core.models import ONGs, Incidents
from django.core.paginator import Paginator
from django.views.generic import View


@method_decorator(csrf_exempt, name='dispatch')
class OngsView(View):
    def get(self, request):
        all_ongs = ONGs.objects.all()
        ongs = []
        for ong in all_ongs:
            ongs.append({
                'id': ong.id,
                'name': ong.name,
                'email': ong.email,
                'whatsapp': ong.whatsapp,
                'city': ong.city,
                'uf': ong.uf
            })

        return JsonResponse(ongs, safe=False)

    def post(self, request):
        body = loads(request.body)

        try:
            ong = ONGs(
                name=body['name'],
                email=body['email'],
                whatsapp=body['whatsapp'],
                city=body['city'],
                uf=body['uf']
            )

            ong.save()

        except KeyError:
            return JsonResponse({'Fail': 'Data is missing.'}, status=400)

        return JsonResponse({'id': ong.id}, status=201, safe=False)


@csrf_exempt
def incidents(request):
    if request.method == 'POST':
        data = loads(request.body)

        try:
            ong = request.headers['Authorization']

            if not ONGs.objects.filter(id=ong):
                return JsonResponse({'Error': 'Ong invalid.'}, status=400)

            ong = ONGs.objects.get(id=ong)

            incident = Incidents(
                title=data['title'],
                description=data['description'],
                value=data['value'],
                ong=ong
            )

            incident.save()

        except KeyError:
            return JsonResponse({'Fail': 'Data is missing.'}, status=400)

        return JsonResponse({'id': incident.id}, status=201, safe=False)

    all_incidents = Incidents.objects.all()
    incidents = []
    for i, incident in enumerate(all_incidents):
        ong = ONGs.objects.get(id=incident.ong_id)
        incidents.append({
            'id': incident.id,
            'title': incident.title,
            'description': incident.description,
            'value': incident.value,
            'ong': incident.ong_id,
            'name': ong.name,
            'email': ong.email,
            'whatsapp': ong.whatsapp,
            'city': ong.city,
            'uf': ong.uf
        })

    if 'page' in request.GET:
        page = request.GET['page']
        incidents = Paginator(incidents, 5)

        return JsonResponse(incidents.page(page).object_list, safe=False)
    return JsonResponse(incidents, safe=False)


@csrf_exempt
def incident(request, id):
    if request.method == 'DELETE':
        ong_id = request.headers['Authorization']
        incident = Incidents.objects.get(id=id)
        if incident.ong_id == int(ong_id):
            incident.delete()
            return JsonResponse({'DELETE': id}, safe=False, status=204)

        return JsonResponse({'Error': 'Operation not permitted'},
                            safe=False, status=401)


@csrf_exempt
def list_incidents_from_an_ong(request):
    if request.method == 'GET':
        ong_id = request.headers['Authorization']
        all_incidents = Incidents.objects.filter(ong_id=ong_id)
        incidents = []
        for incident in all_incidents:
            incidents.append({
                'id': incident.id,
                'title': incident.title,
                'description': incident.description,
                'value': incident.value,
                'ong': incident.ong_id,
            })

        return JsonResponse(incidents, safe=False)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = loads(request.body)

        ong = ONGs.objects.get(id=data['id'])

        return JsonResponse({'name': ong.name}, safe=False)
