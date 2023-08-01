from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from main.models import Task
from .user import UserFactory


class TaskFactory(DjangoModelFactory):
    title = Faker("text")
    description = Faker("text")
    author = SubFactory(UserFactory)
    performer = SubFactory(UserFactory)
    final_date = Faker("date")
    priority = Faker("text")

    class Meta:
        model = Task

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.add(*extracted)
