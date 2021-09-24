from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from chat.models import Room
from chat.factories import RoomFactory


User = get_user_model()


class ChatRoomTemplateTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ChatRoomTemplateTests, cls).setUpClass()
        cls.user = UserFactory.create()

    def test_chat_room_list_template(self):
        response = self.client.get(reverse('chat_room_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_room_list.html')

    def test_chat_room_template(self):
        self.client.force_login(self.user)
        room = RoomFactory.create()
        response = self.client.get(reverse('chat_room', kwargs={'room_id': room.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat_room.html')


class ChatRoomListTest(TestCase):

    def test_active_chat_list(self):
        users = UserFactory.create_batch(3)
        active_chat_rooms = RoomFactory.create_batch(2, users=users)
        RoomFactory.create_batch(2, status=Room.RoomStatus.REMOVED)
        RoomFactory.create_batch(2, status=Room.RoomStatus.HIDDEN)
        response = self.client.get(reverse('chat_room_list'))
        self.assertCountEqual(list(response.context_data['chat_rooms']), active_chat_rooms)


class ChatRoomTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ChatRoomTest, cls).setUpClass()
        cls.user = UserFactory.create()
        cls.room = RoomFactory.create()

    def test_200_if_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('chat_room', kwargs={'room_id': self.room.id}))
        self.assertEqual(response.status_code, 200)

    def test_302_if_not_authenticated(self):
        response = self.client.get(reverse('chat_room', kwargs={'room_id': self.room.id}))
        self.assertEqual(response.status_code, 302)
