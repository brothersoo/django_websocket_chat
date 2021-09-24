from mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories import UserFactory
from chat.models import Room
from chat.tests.factories import RoomFactory


User = get_user_model()


class ChatRoomListTest(TestCase):

    def test_active_chat_list(self):
        users = UserFactory.create_batch(3)
        active_chat_rooms = RoomFactory.create_batch(2, users=users)
        RoomFactory.create_batch(2, status=Room.RoomStatus.REMOVED)
        RoomFactory.create_batch(2, status=Room.RoomStatus.HIDDEN)
        response = self.client.get(reverse('chat_room_list'))
        self.assertCountEqual(list(response.context_data['chat_rooms']), active_chat_rooms)

