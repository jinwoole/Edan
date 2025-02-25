from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import LLMModel, LLMApiKey
from django.http import JsonResponse
import json

@staff_member_required
def model_list(request):
    models = LLMModel.objects.all().order_by('provider', 'name')
    return render(request, 'llm/model_list.html', {'models': models})

@staff_member_required
def api_key_list(request):
    api_keys = LLMApiKey.objects.all().order_by('provider', 'name')
    return render(request, 'llm/api_key_list.html', {'api_keys': api_keys})

@staff_member_required
def test_llm_connection(request, model_id):
    model = get_object_or_404(LLMModel, id=model_id)
    
    from chat.services.llm_service import LLMService
    
    llm_service = LLMService(model.name)
    
    try:
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]
        response = llm_service.generate_response(test_messages)
        return JsonResponse({'success': True, 'response': response})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})