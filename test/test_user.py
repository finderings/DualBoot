from test.base import TestViewSetBase
import factory
from test.fixtures.factories.user import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
    another_user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
    user_attributes["first_name"] = "Johnny"
    another_user_attributes["first_name"] = "Jimmy"
    del user_attributes["role"]
    
    def setUp(self) -> None:
        super().setUp()
        self.user = self.create(self.user_attributes)
        
    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes,
                "id": entity["id"],
                "phone": entity["phone"],
                }

    def test_create(self):
        expected_response = self.expected_details(
            self.user,
            self.user_attributes)

        assert self.user == expected_response

    def test_delete(self):
        deleted_user = self.delete(self.user["id"])

        assert deleted_user == None

    def test_retrieve(self):
        retrieved_data = self.retrieve(self.user["id"])

        assert self.user == retrieved_data

    def test_update(self):
        updated_data = self.update(
            self.another_user_attributes, key=self.user["id"]
            )

        assert updated_data["first_name"] == "Jimmy"

    def test_list(self):
        data = self.list()

        assert len(data) == 1

    def test_filter(self):
        data = self.filter({"first_name": "John"})

        expected_response_match = self.expected_details(
            self.user, self.user_attributes
            )
        expected_response_no_match = self.expected_details(
            self.user, self.another_user_attributes
            )

        assert expected_response_match in data
        assert expected_response_no_match not in data

    def test_unauthorized(self):
        self.check_authorization(self.user["id"])
