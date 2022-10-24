from email import message
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.models import Room

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'room1'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
    

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'][0]
        room_name = Room.objects.get(pk=text_data_json['message'][1]).room_name
        


        async_to_sync(self.channel_layer.group_send)(
            room_name,
            {
                'type':'chat_function',
                'message': message
            }
        )
    def chat_function(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))