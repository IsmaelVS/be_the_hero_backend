"""Receives requests and returns responses."""
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
    """Class Based Views to ONGs."""

    def get(self, request) -> dict:
        """List all ONGs."""
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

    def post(self, request) -> dict:
        """Create new ONG."""
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


@method_decorator(csrf_exempt, name='dispatch')
class IncidentsView(View):
    """Class Based Views to Incidents."""

    def get(self, request) -> dict:
        """List all Incidents."""
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

            if int(page) > incidents.num_pages:
                return JsonResponse(
                    {'Error': 'Invalid pagination.'}, status=400)

            return JsonResponse(incidents.page(page).object_list, safe=False)
        return JsonResponse(incidents, safe=False)

    def post(self, request) -> dict:
        """Create new incident."""
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


@method_decorator(csrf_exempt, name='dispatch')
class DeleteIncidentView(View):
    """Class Based Views to deletar Incidents."""

    def delete(self, request, id) -> dict:
        """Delete incident."""
        if not 'Authorization' in request.headers:
            return JsonResponse(
                {'Error': 'Operation not permitted.'}, status=401)

        ong_id = request.headers['Authorization']

        if not Incidents.objects.filter(id=id):
            return JsonResponse({'Error': 'Incident invalid.'}, status=400)

        incident = Incidents.objects.get(id=id)

        if incident.ong_id == int(ong_id):
            incident.delete()
            return JsonResponse({'DELETE': id}, safe=False, status=204)

        return JsonResponse({'Error': 'Operation not permitted.'},
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
