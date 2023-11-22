import json

from channels.generic.websocket import WebsocketConsumer

from chatbot.chat import get_chatbot_message

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        chat_response = get_chatbot_message(message)
        self.send(text_data=json.dumps({ "message": message, "response": chat_response}))

    # def chat_message(self, event):
    #     message = event['message']

    #     self.send(text_data=json.dumps({
    #         'type':'chat',
    #         'message':message
    #     }))

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        chat_response = get_chatbot_message(message)
        self.send(text_data=json.dumps({ "message": message, "response": chat_response}))