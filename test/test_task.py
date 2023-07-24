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
        self.another_task_attributes = {
            "title": "new_title",
            "description": "new_description",
            "priority": "low",
            "final_date": "2025-05-05",
            "author": self.author.id,
            "performer": self.performer.id,
            "tags": [self.tag.id],
        }
        self.task = self.create(self.task_attributes)

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
            "performer": entity["performer"],
            "date_changed": entity["date_changed"],
            "date_created": entity["date_created"],
        }
        return returned_data

    def test_create(self):
        expected_response = self.expected_details(
            self.task, self.task_attributes
            )

        assert self.task == expected_response

    def test_delete(self):
        deleted_task = self.delete(self.task["id"])

        assert deleted_task == None

    def test_retrieve(self):
        retrieved_data = self.retrieve(self.task["id"])

        assert self.task == retrieved_data

    def test_update(self):
        updated_data = self.update(
            self.another_task_attributes, key=self.task["id"]
            )

        assert updated_data["title"] == "new_title"

    def test_list(self):
        self.create(self.another_task_attributes)

        data = self.list()

        assert len(data) == 2

    def test_filter(self):
        wrong_task = self.create(self.another_task_attributes)
        data = self.filter({"title": "test"})

        expected_response_match = self.expected_details(
            self.task, self.task_attributes
            )
        expected_response_no_match = self.expected_details(
            wrong_task, self.another_task_attributes
        )

        assert expected_response_match in data
        assert expected_response_no_match not in data

    def test_unauthorized(self):
        self.check_authorization(self.task["id"])
