from factory import Faker
from factory.django import DjangoModelFactory

from main.models import Tag


class TagFactory(DjangoModelFactory):
    title = Faker("text")

    class Meta:
        model = Tag
