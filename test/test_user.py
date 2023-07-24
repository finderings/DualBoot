from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "date_of_birth": "1990-01-01",
        "phone": "+33211234545"
    }
    another_user_attributes = {
        "username": "Jimsmith",
        "first_name": "Jim",
        "last_name": "Smith",
        "email": "john@test.com",
        "date_of_birth": "1990-01-01",
        "phone": "+33211234545"
    }
    
    def setUp(self) -> None:
        super().setUp()
        self.user = self.create(self.user_attributes)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        expected_response = self.expected_details(
            self.user, self.user_attributes
            )

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

        assert updated_data["first_name"] == "Jim"

    def test_list(self):
        data = self.list()

        assert len(data) == 3

    def test_filter(self):
        wrong_user = self.create(self.another_user_attributes)
        data = self.filter({"username": "john"})

        expected_response_match = self.expected_details(
            self.user, self.user_attributes
            )
        expected_response_no_match = self.expected_details(
            wrong_user, self.another_user_attributes
            )

        assert expected_response_match in data
        assert expected_response_no_match not in data

    def test_unauthorized(self):
        self.check_authorization(self.user["id"])
