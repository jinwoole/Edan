from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
import json
import uuid

def index(request):
    if not request.user.is_authenticated:
        # 비로그인 사용자는 빈 목록 표시
        conversations = []
    else:
        conversations = Conversation.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-updated_at')[:10]
    
    return render(request, 'chat/index.html', {
        'conversations': conversations
    })

@login_required
def create_conversation(request):
    default_system_prompt = "당신은 유용한 AI 어시스턴트입니다. 사용자의 질문에 정확하고 도움이 되는 답변을 제공하세요."
    
    conversation = Conversation.objects.create(
        user=request.user,
        title="새 대화",
        system_prompt=default_system_prompt
    )
    
    return redirect('chat:conversation', conversation_id=conversation.id)

@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # 자신의 대화만 볼 수 있음
    if conversation.user != request.user:
        return redirect('chat:index')
    
    messages = conversation.messages.all().order_by('created_at')
    
    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'messages': messages
    })

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # 자신의 대화만 메시지 보낼 수 있음
    if conversation.user != request.user:
        return HttpResponse("권한이 없습니다", status=403)
    
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
    except:
        message_content = request.POST.get('message', '').strip()
    
    if not message_content:
        return HttpResponse("메시지를 입력하세요", status=400)
    
    message = Message.objects.create(
        conversation=conversation,
        role='user',
        content=message_content,
        tokens=len(message_content.split()) * 1.5
    )
    
    response = render(request, 'chat/components/message_list.html', {
        'conversation': conversation,
        'messages': conversation.messages.all().order_by('created_at')
    })
    
    response['HX-Trigger'] = json.dumps({
        'newMessage': {
            'id': str(message.id),
            'conversationId': str(conversation.id)
        }
    })
    
    return response

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # 자신의 대화만 삭제 가능
    if conversation.user != request.user:
        return JsonResponse({"error": "unauthorized"}, status=403)
    
    conversation.is_active = False
    conversation.save()
    
    # HTMX 요청인 경우 빈 응답 반환
    if request.headers.get('HX-Request'):
        return HttpResponse("")
    
    return redirect('chat:index')

@login_required
def update_conversation_title(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # 자신의 대화만 제목 수정 가능
    if conversation.user != request.user:
        return JsonResponse({"error": "unauthorized"}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_title = data.get('title', '').strip()
        except:
            new_title = request.POST.get('title', '').strip()
        
        if new_title:
            conversation.title = new_title
            conversation.save()
            return JsonResponse({"success": True})
    
    return JsonResponse({"error": "invalid request"}, status=400)