from django.db import models

class LLMModel(models.Model):
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    api_key_variable = models.CharField(max_length=100, blank=True)
    api_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    context_window = models.IntegerField(default=4096)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'llm_models'

class LLMApiKey(models.Model):
    key = models.CharField(max_length=255)
    provider = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'llm_api_keys'