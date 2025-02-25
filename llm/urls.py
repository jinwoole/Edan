from django.urls import path
from . import views

app_name = 'llm'

urlpatterns = [
    path('models/', views.model_list, name='model_list'),
    path('api-keys/', views.api_key_list, name='api_key_list'),
    path('test-connection/<int:model_id>/', views.test_llm_connection, name='test_connection'),
]
