from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_conversation, name='create_conversation'),
    path('conversation/<uuid:conversation_id>/', views.conversation, name='conversation'),
    path('conversation/<uuid:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversation/<uuid:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('conversation/<uuid:conversation_id>/update-title/', views.update_conversation_title, name='update_title'),
]