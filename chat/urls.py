from django.urls import path

from .views import ChatListView, ChatRoomView, index

urlpatterns = [
    path('', index, name='index'),
    path('list/', ChatListView.as_view(), name='chat_room_list'),
    path('<int:room_id>/', ChatRoomView.as_view(), name='chat_room')
]
