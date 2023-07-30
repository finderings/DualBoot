from factory import Factory, Faker

from main.models import Task


class TaskFactory(Factory):
    title = Faker("text")
    description = Faker("text")
    author = Faker("first_name")
    performer = Faker("last_name")
    final_date = Faker("date")
    tags = Faker("text")
    priority = Faker("text")

    class Meta:
        model = Task
