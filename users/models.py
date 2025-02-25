from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    preferred_model = models.ForeignKey('llm.LLMModel', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'users'