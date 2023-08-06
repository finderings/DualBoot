from test.base import TestViewSetBase
import factory
from test.fixtures.factories.task import TaskFactory


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)
    another_task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)
    task_attributes["title"] = "test_title"
    another_task_attributes["title"] = "new_title"

    def setUp(self) -> None:
        super().setUp()
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
        del self.task["author"]
        del self.task["performer"]

        retrieved_data = self.retrieve(self.task, self.task["id"])
        del retrieved_data["author"]
        del retrieved_data["performer"]
        
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
        data = self.list({"title": "test"})

        expected_response_match = self.expected_details(
            self.task, self.task_attributes
            )
        expected_response_no_match = self.expected_details(
            self.task, self.another_task_attributes
        )

        assert expected_response_match in data
        assert expected_response_no_match not in data

    def test_unauthorized(self):
        self.check_authorization(self.task["id"])
