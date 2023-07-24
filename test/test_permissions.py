from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Tag, Task
from test.base import UserFactory, SuperUserFactory


class TestPerm(APITestCase):
    client: APIClient
    admin: SuperUserFactory
    user: UserFactory
    models: list = [Tag, Task]
    token_url = reverse("token_obtain_pair")

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = SuperUserFactory.create()
        cls.user = UserFactory.create()
        cls.client = APIClient()

    def assert_methods_status(self, method: str, response_status: int) -> None:
        for model in self.models:
            obj = model.objects.create()
            url = reverse(f"{model._meta.model_name}s-detail", args=(obj.id,))

        response = self.client.__getattribute__(method)(url)
        assert response.status_code == response_status

    def token_request(self, username: str = None, password: str = "password"):
        client = self.client_class()
        if not username:
            username = self.UserFactory.create().username
        return client.post(
            self.token_url, data={"username": username, "password": password}
            )

    def test_isdelete_permission_user(self) -> None:
        token = self.token_request(self.user.username)
        self.client.force_authenticate(user=self.user, token=token)

        self.assert_methods_status("get", HTTPStatus.OK)
        self.assert_methods_status("delete", HTTPStatus.FORBIDDEN)

    def test_isdelete_permisiion_admin(self) -> None:
        token = self.token_request(self.admin.username)
        self.client.force_authenticate(user=self.admin, token=token)
        
        self.assert_methods_status("delete", HTTPStatus.NO_CONTENT)
