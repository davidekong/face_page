from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length = 100, default = 'room'+str(id))

class Message(models.Model):
    message = models.CharField(max_length = 1000)
    sender = models.CharField(max_length = 100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
