import json
from .models import ChatMessage, Connection
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
# Create your views here.
@csrf_exempt
def test(request):
    return JsonResponse({'message':'Hello Daud'}, status=200)

def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)
@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.create(connection_id=connection_id)
    response = {
        "statusCode": 200,
        "body": "Connecte succesfully"
    }
    # return response
    return JsonResponse('connect successfully', status=200, safe=False)
@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.get(connection_id=connection_id).delete()
    return JsonResponse('disconnect successfully', status=200, safe=False)

def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client('apigatewaymanagementapi', 
    endpoint_url= "https://gr3cwo64fb.execute-api.us-west-2.amazonaws.com/Test/",
    region_name='us-west-2',
    aws_access_key_id='',
    aws_secret_access_key= '')
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))
@csrf_exempt
def send_message(request):
    body = _parse_body(request.body) 
    ChatMessage.objects.create(username=body['username'], message=body['message'], timestamp=body['timestamp'])
    connections = [i.connection_id for i in Connection.objects.all()]
    data = {'messages':[body]}
    for connection in connections:
        _send_to_connection(connection, data)
    return JsonResponse('successfully sent', status=200, safe=False)
@csrf_exempt
def get_recent_messages(request):
    body = _parse_body(request.body)
    connectionId = body['connectionId']
    connection_id = Connection.objects.get(connection_id=connectionId)
    messages = ChatMessage.objects.all()
    data = {'messages':[{'username':connection.username, 'message':connection.message,
    'timestamp':connection.timestamp} for message in messages]}
    _send_to_connection(connection_id, data )
    return JsonResponse('successfully sent', status=200)


