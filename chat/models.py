from django.db import models
from django.conf import settings
import uuid

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    llm_model = models.ForeignKey('llm.LLMModel', on_delete=models.SET_NULL, null=True)
    system_prompt = models.TextField(blank=True)
    
    summary = models.TextField(blank=True)
    key_points = models.JSONField(default=list, blank=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']

class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    tokens = models.IntegerField(default=0)
    is_summary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']