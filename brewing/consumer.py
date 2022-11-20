import json
from brewing.models import brew_recipe
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .views import brew_system
import asyncio


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        self.task = []
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        brew_system.write_to_log("Another client connected")
        self.send_json({'type': 'chat_message', 'message': json.dumps(
            brew_system.get_status(), indent=4)})

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.evaluate_response(text_data_json)

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type':'chat_message',
        #         'message':message
        #     }
        # )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def evaluate_response(self, msg):
        command = msg['command']
        if(command == "get_status"):
            self.send_json(
                {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
        elif(command == "keep_process"):
            brew_system.keep_process()
            self.send_json(
                {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
        elif(command == "next"):
            if(brew_system.next_step()):
                print("loaded next step")
                self.send_json(
                    {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
            else:
                self.send_json(
                    {'type': 'chat_message', 'message': '{"error": "error encaunterd while loading next step"}'})
                print("error encaunterd while loading next step")

        elif(command == "start"):
            if(brew_system.start_process()):
                print("started process")
                self.send_json(
                    {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
            else:
                print("error encaunterd while trying to start the process")
        elif(command == "reset"):
            if(brew_system.stop_process()):
                print("process reset")
                brew_system.manual_engine("off")
                brew_system.heat(0)
                exit()
                # self.send_json(
                #     {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
            else:
                print("error encaunterd while reseting the process")
        elif(command == "getRecipe"):
            print(int(msg["message"]))
            rec = brew_recipe.objects.get(id=int(msg["message"]))
            self.send_json(
                    {'type': 'chat_message', 'message': json.dumps(rec.getRecipe())})
        elif(command == "manual_engine"):
            brew_system.manual_engine(msg['message'])
            self.send_json(
                    {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
        elif(command == "manual_temp"):
            brew_system.heat(float(msg['message']))
            self.send_json(
                    {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
        elif(command == "prev"):
            if(brew_system.step_back()):
                print("loaded previous step")
                self.send_json(
                    {'type': 'chat_message', 'message': json.dumps(brew_system.get_status())})
            else:
                print("error encaunterd while loading previous step")
        # error = {
        #     "message": "Unknown command",
        # }
        # self.send_json({'message':json.dumps(error)})

    def stop(self):
        """
        stops the procedure
        """
        self.task.cancel()
        self.reset()

    def reset(self):
        """
        resets the timer
        """
        print('reseted')

    def send_json(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )
