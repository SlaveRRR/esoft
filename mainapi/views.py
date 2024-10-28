from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from mainapi.models import Events, Events_Types
from mainapp.models import User
# from mainapi import serialisers
from mainapi.serializers import Events_TypesSerializer, EventsSerialiser
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
import redis
from datetime import datetime
from datetime import date,time
from django.contrib.auth import authenticate, login,logout
from django.utils.timezone import make_aware

import random
import string
import ast
import json

redis_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@csrf_exempt
def registrate(request):
    if request.method == 'POST':
        
        json_data = json.loads(request.body)
        nickname = json_data['nickname']
        password = json_data['password']
        user = authenticate(request, nickname=nickname, password=password)
        if user:
            key = generate_key()
            redis_storage.set(key, user.id)
            return JsonResponse({'status':"200",'token':key,'user':user.id})
        else: return JsonResponse({'status':"400",'error':"User not found",'json_data':json_data})
    else: return JsonResponse({'status':"400",'error':"Method not allowed"})

def generate_key(length=6):
    # cursor = connection.cursor()
    characters = string.ascii_letters + string.digits
    unique_string = ''.join(random.choice(characters) for _ in range(length))
    # cursor.execute("SELECT `BookingReference` FROM `tickets`")
    # keys = list(cursor.fetchall())
    return unique_string
    # if unique_string not in keys:
        
    # else:
    #     unique_string = generate_key(length=6)
    #     return unique_string

@csrf_exempt
def get_events(request):
    json_data = json.loads(request.body)
    user = int(json_data['user'])
    # token = json_data['token']

    # user = request.POST['user']
    # print("datetime.now()",date.today())
    if user:
        # '2023-12-08 22:42:36.000000'
        # >= datetime.now().date ,user_id = user
        # today_min = datetime.combine(date.today(), time.min)
        # today_max = datetime.combine(date.today(), time.max)
        queryset = Events.objects.filter(event_take__date = date.today(), user_id = user)
        serialiser = EventsSerialiser(queryset,many=True)
        return JsonResponse({'events':serialiser.data})

@csrf_exempt
def delete_event(request):
    json_data = json.loads(request.body)
    id = int(json_data['id'])
    if id:
        queryset = Events.objects.get(id=id)
        queryset.delete()
        return JsonResponse({'status':'300','result':'successfully deleted'})

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        user = json_data['user']
        if user:
            event_take = json_data['event_take']
            event_length = json_data['event_length']
            event_type = json_data['event_type']
            comment = json_data['comment']

            event = Events(None,event_take,event_length,event_type,comment,user)
            event.save()
    return JsonResponse({'status':'300','result':'successfully created'})



# Create your views here.
