from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from chat.models import Room


class RoomFactory(DjangoModelFactory):
    title = Faker('sentence', nb_words=3)

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)

    class Meta:
        model = Room
