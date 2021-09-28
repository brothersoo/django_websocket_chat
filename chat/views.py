from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.query import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from chat.forms import RoomCreateForm
from chat.models import Room, Participate
from chat.utils import participate


User = get_user_model()


class ChatListView(TemplateView):
    template_name = 'chat/chat_room_list.html'
    queryset = None

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = Room.objects.filter(status=Room.RoomStatus.ACTIVE)\
                .annotate(participant_count=Count('users'))\
                .order_by('-created_at')
        return self.queryset

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'chat_rooms': self.get_queryset()
        })


class ChatRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/chat_room.html'
    queryset = Room.objects.filter(status=Room.RoomStatus.ACTIVE)

    def get(self, request, *args, **kwargs):
        instance: Room = Room.objects.prefetch_related(
            Prefetch(
                'participate_set',
                queryset=Participate.objects.select_related('user').filter(
                    status=Participate.ParticipateStatus.PARTICIPATING
                )
            )
        ).annotate(participant_count=Count('users')).get(id=self.kwargs['room_id'])

        participate(instance, request.user)

        return self.render_to_response({
            'room': instance,
            'user_nickname': request.user.nickname,
            'participants': instance.participate_set.values_list('user__nickname', flat=True)
        })


class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomCreateForm
    template_name_suffix = '_create_form'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('chat_room', kwargs={'room_id': self.object.id})
