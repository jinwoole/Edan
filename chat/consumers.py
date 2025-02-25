import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from .services.llm_service import LLMService
from .services.context_manager import ContextManager
import uuid

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        user_message = await self.save_user_message(message)
        
        context_manager = ContextManager(self.conversation_id)
        
        llm_messages = await database_sync_to_async(context_manager.get_messages_for_llm)()
        
        llm_service = LLMService()
        response = await llm_service.generate_response(llm_messages)
        
        assistant_message = await self.save_assistant_message(response)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response,
                'message_id': str(assistant_message.id)
            }
        )
        
        await database_sync_to_async(context_manager.summarize_conversation)()
    
    async def chat_message(self, event):
        message = event['message']
        message_id = event['message_id']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'message_id': message_id
        }))
    
    @database_sync_to_async
    def save_user_message(self, content):
        return Message.objects.create(
            conversation_id=self.conversation_id,
            role='user',
            content=content,
            tokens=len(content.split()) * 1.5
        )
    
    @database_sync_to_async
    def save_assistant_message(self, content):
        return Message.objects.create(
            conversation_id=self.conversation_id,
            role='assistant',
            content=content,
            tokens=len(content.split()) * 1.5
        )
