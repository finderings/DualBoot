from http import HTTPStatus

from test.base import TestViewSetBase
from test.fixtures.factories.user import UserFactory
from test.fixtures.factories.task import TaskFactory

from django.forms.models import model_to_dict


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"

    def test_list(self) -> None:
        user = UserFactory.create()
        task1 = model_to_dict(TaskFactory.create(performer=user))
        task1_id = task1['id']

        tasks = self.list(args=[user.id])
        
        assert any(task['id'] == task1_id for task in tasks)

    def test_retrieve_foreign_task(self) -> None:
        user = UserFactory.create()
        task = TaskFactory.create()

        response = self.request_retrieve(key=[user.id, task.id])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        user = UserFactory.create()
        task = model_to_dict(TaskFactory.create(performer=user))

        retrieved_task = self.retrieve(task, key=[user.id, task['id']])

        assert task['id'] == retrieved_task['id']

    def test_delete(self) -> None:
        user = UserFactory.create()
        task = TaskFactory.create(performer=user)

        deleted_task = self.delete(key=[user.id, task.id])
        
        assert deleted_task == None

    def test_update(self) -> None:
        user = UserFactory.create()
        task = TaskFactory.create(performer=user)
        updated_data = {"title": "new_title",
                        "description": "description",
                        "priority": "low",
                        }

        updated_task = self.update(data=updated_data, key=[user.id, task.id])

        assert updated_task["title"] == "new_title"
