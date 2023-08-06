from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from main.models import Task
from .user import UserFactory


class TaskFactory(DjangoModelFactory):
    title = Faker("text", max_nb_chars=7)
    description = Faker("text", max_nb_chars=7)
    author = SubFactory(UserFactory)
    performer = SubFactory(UserFactory)
    final_date = Faker("date")
    priority = Faker("text", max_nb_chars=7)

    class Meta:
        model = Task

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tags.add(*extracted)
