from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='chat_room_list', permanent=False)),
    path('chat/', include('chat.urls')),
    path('accounts/', include('accounts.urls')),
]
