from http import HTTPStatus

from main.models import Task

from test.base import TestViewSetBase
from test.fixtures.factories.task import TaskFactory
from test.fixtures.factories.tag import TagFactory

from django.forms.models import model_to_dict


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"

    def add_tags(self, task: dict, tags: list) -> None:
        task_instance = Task.objects.get(pk=task.id)
        for tag in tags:
            task_instance.tags.add(tag['id'])
        task_instance.save()

    def test_list(self) -> None:
        task = TaskFactory.create()
        tag1 = model_to_dict(TagFactory.create())
        tag2 = model_to_dict(TagFactory.create())
        self.add_tags(task, [tag1, tag2])

        tags = self.list(args=[task.id])

        assert tags == [tag1, tag2]

    def test_retrieve_foreign_tag(self) -> None:
        task = TaskFactory.create()
        tag = TagFactory.create()

        response = self.request_retrieve(key=[task.id, tag.id])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        task = TaskFactory.create()
        tag = model_to_dict(TagFactory.create())
        self.add_tags(task, [tag])

        retrieved_tag = self.retrieve(tag, key=[task.id, tag['id']])

        assert tag['id'] == retrieved_tag['id']

    def test_delete(self) -> None:
        task = TaskFactory.create()
        tag = model_to_dict(TagFactory.create())
        self.add_tags(task, [tag])

        deleted_tag = self.delete(key=[task.id, tag['id']])
        
        assert deleted_tag == None

    def test_update(self) -> None:
        task = TaskFactory.create()
        tag = model_to_dict(TagFactory.create())
        self.add_tags(task, [tag])
        updated_data = {"title": "new_title"}

        updated_tag = self.update(data=updated_data, key=[task.id, tag["id"]])

        assert updated_tag["title"] == "new_title"
