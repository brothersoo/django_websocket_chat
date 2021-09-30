from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from faker import Faker

from accounts.factories import UserFactory
from chat.models import Room
from chat.factories import RoomFactory


User = get_user_model()

faker = Faker()


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

    def test_chat_list_participant_count(self):
        creator = UserFactory.create()
        participants = UserFactory.create_batch(3)
        RoomFactory.create(users=participants, creator=creator)
        response = self.client.get(reverse('chat_room_list'))
        self.assertEqual(response.context_data['chat_rooms'][0].participant_count, 3)


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


class ChatRoomCreateTest(TestCase):
    def test_create_room_redirection(self):
        self.client.force_login(UserFactory.create())
        room_data: dict = {
            'title': faker.sentence(nb_words=1)
        }
        response = self.client.post(reverse('chat_room_create'), data=room_data, follow=True)
        self.assertEqual(response.status_code, 200)

        created_room: Room = response.context_data['room']
        self.assertEqual(response.redirect_chain[-1][0], reverse('chat_room', kwargs={'room_id': created_room.id}))
        self.assertEqual(response.redirect_chain[-1][1], 302)

    def test_create_room_data(self):
        user: User = UserFactory.create()
        self.client.force_login(user)
        room_data: dict = {
            'title': faker.sentence(nb_words=1)
        }
        response = self.client.post(reverse('chat_room_create'), data=room_data, follow=True)

        created_room: Room = response.context_data['room']
        self.assertEqual(created_room.title, room_data['title'])
        self.assertEqual(created_room.status, Room.RoomStatus.ACTIVE)
        self.assertEqual(created_room.users.count(), 0)
        self.assertEqual(created_room.creator, user)
