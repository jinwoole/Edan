from chat.models import Message, Conversation
import json

class ContextManager:
    def __init__(self, conversation_id):
        self.conversation = Conversation.objects.get(id=conversation_id)
    
    def get_messages_for_llm(self, max_tokens=4000):
        messages = list(self.conversation.messages.all().order_by('created_at'))
        
        result = []
        if self.conversation.system_prompt:
            result.append({
                "role": "system",
                "content": self.conversation.system_prompt
            })
        
        total_tokens = sum(msg.tokens for msg in messages)
        
        if total_tokens > max_tokens and self.conversation.summary:
            result.append({
                "role": "system",
                "content": f"이전 대화 요약: {self.conversation.summary}\n\n주요 포인트: {json.dumps(self.conversation.key_points, ensure_ascii=False)}"
            })
            
            recent_tokens = 0
            recent_messages = []
            
            for msg in reversed(messages):
                if recent_tokens + msg.tokens < 2000:
                    recent_messages.insert(0, msg)
                    recent_tokens += msg.tokens
                else:
                    break
                    
            for msg in recent_messages:
                result.append({
                    "role": msg.role,
                    "content": msg.content
                })
        else:
            for msg in messages:
                result.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        return result
    
    async def summarize_conversation(self):
        from .llm_service import LLMService
        
        messages = list(self.conversation.messages.all().order_by('created_at'))
        
        if len(messages) < 10:
            return
        
        prompt = "다음 대화 내용을 200자 이내로 요약하고, 주요 포인트 5개를 추출해주세요.\n\n"
        
        for msg in messages:
            prompt += f"{msg.role.capitalize()}: {msg.content}\n\n"
        
        llm_service = LLMService()
        summary_messages = [
            {"role": "system", "content": "당신은 대화 내용을 간결하게 요약하는 AI 어시스턴트입니다."},
            {"role": "user", "content": prompt}
        ]
        
        summary_response = await llm_service.generate_response(summary_messages)
        
        try:
            summary_part = summary_response.split("주요 포인트")[0].strip()
            points_part = summary_response.split("주요 포인트")[1].strip()
            
            points = []
            for line in points_part.split("\n"):
                if line.strip() and any(c.isdigit() for c in line[:3]):
                    points.append(line.strip())
            
            self.conversation.summary = summary_part
            self.conversation.key_points = points
            self.conversation.save()
        except Exception as e:
            print(f"요약 파싱 오류: {str(e)}")