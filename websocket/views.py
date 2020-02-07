import json
from .models import ChatMessage, Connection
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def test(request):
    return JsonResponse({'message':'Hello Daud'}, status=200)

def _parse_body(body):
    body_unicode = body.decode('utf-8')
@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.create(connection_id=connection_id)
    return JsonResponse('connect successfully', status=200)
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.delete(connection_id=connection_id)
    return JsonResponse('disconnect successfully', status=200)
    
