from factory import Factory, Faker, post_generation
from factory.django import DjangoModelFactory

from ..models import Room, Participate


class RoomFactory(DjangoModelFactory):
    title = Faker('sentence')

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)

    class Meta:
        model = Room
