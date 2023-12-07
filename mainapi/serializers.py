from rest_framework import serializers
from .models import Events, Events_Types

class Events_TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events_Types
        fields = ['id', 'name']


class EventsSerialiser(serializers.ModelSerializer):
    event_type = Events_TypesSerializer(many = False,read_only=True)
    class Meta:
        model = Events
        fields = ['id', 'event_take', 'event_length','event_type','comment']
