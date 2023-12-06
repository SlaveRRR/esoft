from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from mainapi.models import Events, Events_Types
from mainapp.models import User
from mainapi.serializers import Events_TypesSerializer, EventsSerialiser
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
import redis
from datetime import datetime
from django.contrib.auth import authenticate, login,logout

redis_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@csrf_exempt
def registrate(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        password = request.POST['password']
        user = authenticate(request, nickname=nickname, password=password)
        if user:
            key = generate_key()
            redis_storage.set(key, user, timeout=600)
            return JsonResponse({'status':"200",'token':key})
        else: return JsonResponse({'status':"400",'error':"User not found"})
    else: return JsonResponse({'status':"400",'error':"Method not allowed"})

def generate_key(length=6):
    cursor = connection.cursor()
    characters = string.ascii_letters + string.digits
    unique_string = ''.join(random.choice(characters) for _ in range(length))
    cursor.execute("SELECT `BookingReference` FROM `tickets`")
    keys = list(cursor.fetchall())
    if unique_string not in keys:
        return unique_string
    else:
        unique_string = generate_key(length=6)
        return unique_string

@csrf_exempt
def get_events(request):
    token = request.POST['token']
    user = redis_storage.get(token)
    if user:
        queryset = Events.objects.filter(event_take=datetime.now())
        serialiser = EventsSerialiser(queryset,many=True)
        return JsonResponse({'events':serialiser.data})

@csrf_exempt
def delete_event(request):
    token = request.POST['token']
    user = redis_storage.get(token)
    if user:
        id = request.POST['id']
        queryset = Events.objects.get(id=id)
        queryset.delete()
        return JsonResponse({'status':'300','result':'successfully deleted'})

@csrf_exempt
def create_event(request):
    token = request.POST['token']
    user = redis_storage.get(token)
    if user:
        event_take = request.POST['event_take']
        event_length = request.POST['event_length']
        event_type = request.POST['event_type']
        comment = request.POST['comment']

        event = Events(event_take,event_length,event_type,comment)
        event.save()
        return JsonResponse({'status':'300','result':'successfully created'})



# Create your views here.
