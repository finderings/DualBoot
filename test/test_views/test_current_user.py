from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_retrieve(self):
        user = self.single_resource()
        user.pop("avatar_picture")

        assert user == {
            'id': self.admin.id,
            'email': self.admin.email,
            'first_name': self.admin.first_name,
            'last_name': self.admin.last_name,
            'role': self.admin.role,
            'username': self.admin.username,
            'date_of_birth': self.admin.date_of_birth,
            'phone': self.admin.phone,
        }
        print(user)

    def test_patch(self):
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"
