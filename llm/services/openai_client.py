import httpx
import json
import os
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.api_url = api_url or os.getenv('LLM_API_URL', 'https://api.openai.com/v1')
    
    async def chat_completion(self, messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": model,
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
                    return response.json()
                else:
                    logger.error(f"API Error: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            logger.exception(f"Service Error: {str(e)}")
            return None