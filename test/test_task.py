from test.base import TestViewSetBase
from main.models import Tag, User


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"

    def setUp(self) -> None:
        super().setUp()
        self.tag = Tag.objects.create(title="test_tag")
        self.author = User.objects.create(username="user1")
        self.performer = User.objects.create(username="user2")
        self.task_attributes = {
            "title": "test_task",
            "description": "description",
            "priority": "high",
            "final_date": "2025-05-05",
            "author": self.author.id,
            "performer": self.performer.id,
            "tags": [self.tag.id],
        }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        returned_data = {
            **attributes,
            "id": entity["id"],
            "final_date": entity["final_date"],
            "description": entity["description"],
            "priority": entity["priority"],
            "status": entity["status"],
            "tags": entity["tags"],
            "author": entity["author"],
            "performer": entity["author"],
            "date_changed": entity["date_changed"],
            "date_created": entity["date_created"],
        }
        return returned_data

    def test_create(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        print("task:", task)
        print("expected_response:", expected_response)
        assert task == expected_response

    def test_delete(self):
        task = self.create(self.task_attributes)
        deleted_task = self.delete(task["id"])
        assert deleted_task == None

    def test_retrieve(self):
        task = self.create(self.task_attributes)
        retrieved_data = self.retrieve(task["id"])
        assert task == retrieved_data

    def test_update(self):
        task = self.create(self.task_attributes)
        updated_task = {
            "title": "another title",
            "description": "new_description",
            "priority": "very high",
        }
        updated_data = self.update(updated_task, key=task["id"])
        assert updated_data["title"] == "another title"

    def test_list(self):
        second_task = {
            "title": "test1_task",
            "description": "description",
            "priority": "high",
            "final_date": "2025-06-06",
            "author": self.author.id,
            "performer": self.performer.id,
            "tags": [self.tag.id],
            }
        self.create(self.task_attributes)
        self.create(second_task)
        data = self.list()
        assert len(data) == 2

    def test_filter(self):
        task = self.create(self.task_attributes)
        data = self.filter({"priority": "high"})
        expected_response = self.expected_details(task, self.task_attributes)
        assert expected_response in data

    def test_unauthorized(self):
        task = self.create(self.task_attributes)
        self.check_authorization(task["id"])
