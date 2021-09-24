from factory import Factory, Faker
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(DjangoModelFactory):
    email = Faker('ascii_company_email')
    nickname = Faker('user_name')

    class Meta:
        model = User
