from factory import Faker
from factory.django import DjangoModelFactory

from main.models import User
from .base import ImageFileProvider


Faker.add_provider(ImageFileProvider)


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    role = Faker("random_element", elements=User.Roles.values)
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    date_of_birth = Faker("date")
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = User


class SuperUserFactory(UserFactory):
    is_staff = True
