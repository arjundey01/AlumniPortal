from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Chats
import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s'%self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data=json.loads(text_data)
        print(data)
        if data['type']=='message':
            resp={}
            resp['username']=self.scope['user'].username
            resp['text']=data['text']
            message=json.dumps(resp)
            await self.save_chat(resp)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        elif data['type']=='seen':
            await self.update_seen()
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'msg_seen',
                'username':self.scope['user'].username
            }
        )
        

    async def msg_seen(self,event):
        if self.scope['user'].username!=event['username']:
            await self.send(json.dumps({'type':'seen','username':event['username']}))

    async def chat_message(self, event):
        message = event['message']
        message=json.loads(message)
        message['type']='message'
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def save_chat(self,data):
        chat=Chats.objects.get(pk=self.room_name)
        chat_data=json.loads(chat.data)
        data['time']=datetime.now()
        data['id']=chat_data[-1]['id']+1 if len(chat_data) else 0
        chat_data.append(data)
        chat.data=json.dumps(chat_data,cls=DjangoJSONEncoder)
        print(json.loads(json.dumps(data,cls=DjangoJSONEncoder)))
        chat.save()
    

    @database_sync_to_async
    def update_seen(self):
        chat=Chats.objects.get(pk=self.room_name)
        seen=json.loads(chat.last_seen_msg)
        seen[self.scope['user'].username]=len(json.loads(chat.data))
        chat.last_seen_msg=json.dumps(seen)
        chat.save()