from django.db import models

class Events_Types(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    event_take = models.DateTimeField()
    event_length = models.TimeField(null=True)
    event_type =  models.ForeignKey(Events_Types, on_delete=models.CASCADE, related_name="type")
    comment = models.TextField(null=True) 
# Create your models here.
