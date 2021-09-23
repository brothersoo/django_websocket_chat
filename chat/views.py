from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Room


def index(request):
    return render(request, 'chat/index.html', {})


class ChatListView(TemplateView):
    template_name = 'chat/chat_room_list.html'
    queryset = Room.objects.filter(status=Room.RoomStatus.ACTIVE)\
        .annotate(participant_count=Count('users'))\
        .order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'chat_rooms': self.queryset
        })


class ChatRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_room.html'
    queryset = Room.objects.filter(status=Room.RoomStatus.ACTIVE)

    def get(self, request, *args, **kwargs):
        instance = self.queryset.get(id=self.kwargs['room_id'])
        print(type(request.user))
        return self.render_to_response({
            'room': instance,
            'user_nickname': request.user.nickname
        })
