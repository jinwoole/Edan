from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # chat 앱의 URL을 루트에서 시작하도록 변경
    path('chat/', include('chat.urls')),  # 이렇게 변경
    path('users/', include('users.urls')),
    path('llm/', include('llm.urls')),
    # 루트 URL을 채팅 인덱스로 리디렉션
    path('', lambda request: redirect('chat:index')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
