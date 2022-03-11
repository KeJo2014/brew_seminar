import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .process.brew_server import brew_server

brew_server = brew_server()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        brew_server.write_to_log("Another client connected")
        self.send_json({'type':'chat_message', 'message':json.dumps(brew_server.get_status())})
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.evaluate_response(message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))

    def evaluate_response(self, command):
        if(command == "get_status"):
            self.send_json({'type':'chat_message', 'message':json.dumps(brew_server.get_status())})
        elif(command == "load_test"):
            brew_server.load_recipe(1)      #add real recipe id
            self.send_json({'type':'chat_message', 'message':json.dumps(brew_server.get_status())})
        self.send_json({'type':'chat_message', 'message':'unauthorized'})
    
    def send_json(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )
    