from django.urls import path

from chat.views import ChatListView, ChatRoomView, ChatRoomCreateView

urlpatterns = [
    path('list/', ChatListView.as_view(), name='chat_room_list'),
    path('<int:room_id>/', ChatRoomView.as_view(), name='chat_room'),
    path('create/', ChatRoomCreateView.as_view(), name='char_room_create'),
]
