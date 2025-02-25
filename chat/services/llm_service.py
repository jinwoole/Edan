import httpx
import os
import json
import logging
from django.conf import settings
from llm.models import LLMModel, LLMApiKey

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_name=None):
        self.model = self._get_model(model_name)
        self.api_key = self._get_api_key()
        self.api_url = self.model.api_url if self.model.api_url else os.getenv('LLM_API_URL', 'http://localhost:8000/v1')
    
    def _get_model(self, model_name):
        if model_name:
            try:
                return LLMModel.objects.get(name=model_name, is_active=True)
            except LLMModel.DoesNotExist:
                pass
        return LLMModel.objects.filter(is_active=True).first()
    
    def _get_api_key(self):
        key_var = self.model.api_key_variable
        if key_var:
            return os.getenv(key_var)
        
        api_key = LLMApiKey.objects.filter(provider=self.model.provider, is_active=True).first()
        if api_key:
            return api_key.key
        
        return None
    
    async def generate_response(self, messages, temperature=0.7, max_tokens=1000):
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": self.model.name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    logger.error(f"LLM API 오류: {response.status_code} - {response.text}")
                    return "죄송합니다, 응답을 생성하는 중 오류가 발생했습니다."
        except Exception as e:
            logger.exception(f"LLM 서비스 오류: {str(e)}")
            return "죄송합니다, 서비스에 연결할 수 없습니다."