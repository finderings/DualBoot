from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_delete(self):
        user = self.create(self.user_attributes)
        deleted_user = self.delete(user["id"])
        assert deleted_user == None

    def test_retrieve(self):
        user = self.create(self.user_attributes)
        retrieved_data = self.retrieve(user["id"])
        assert user == retrieved_data

    def test_update(self):
        user = self.create(self.user_attributes)
        updated_user = {"first_name": "Valera", "username": user["username"]}
        updated_data = self.update(updated_user, key=user["id"])
        assert updated_data["first_name"] == "Valera"

    def test_list(self):
        data = self.list()
        assert len(data) == 2

    def test_filter(self):
        user = self.create(self.user_attributes)
        data = self.filter({"username": "john"})
        expected_response = self.expected_details(user, self.user_attributes)
        assert expected_response in data

    def test_unauthorized(self):
        user = self.create(self.user_attributes)
        self.client.logout()
        self.check_authorization(user["id"])
