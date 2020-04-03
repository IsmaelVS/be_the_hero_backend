from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'POST':
        return HttpResponse("POST")
    if request.method == 'PUT':
        return HttpResponse("PUT")
    if request.method == 'DELETE':
        return HttpResponse("DELETE")
    return HttpResponse("Hello world!")
