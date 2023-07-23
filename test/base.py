from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User
from factory.django import DjangoModelFactory
from factory import PostGenerationMethodCall, Faker


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class SuperUserFactory(UserFactory):
    is_staff = True


class TestViewSetBase(APITestCase):
    user: UserFactory = None
    client: APIClient = None
    basename: str
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.admin = cls.create_api_admin()
        cls.client = APIClient()

    def setUp(self) -> None:
        super().setUp()
        token = self.token_request(self.user.username)
        self.client.force_authenticate(user=self.admin, token=token)

    @classmethod
    def create_api_user(cls):
        return UserFactory.create()

    @classmethod
    def create_api_admin(cls):
        return SuperUserFactory.create()

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(self, arg: List[Union[str, int]] = None) -> dict:
        response = self.client.get(self.list_url(arg))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, key: Union[str, int]) -> dict:
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, key: Union[str, int]) -> dict:
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, key: Union[str, int]) -> None:
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response.data

    def filter(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.get(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def check_authorization(self, key: Union[str, int]) -> None:
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        return response.data

    def token_request(self, username: str = None, password: str = "password"):
        client = self.client_class()
        if not username:
            username = self.create_api_user().username
        return client.post(
            self.token_url, data={"username": username, "password": password}
            )

    def refresh_token_request(self, refresh_token: str):
        client = self.client_class()
        return client.post(
            self.refresh_token_url, data={"refresh": refresh_token}
            )

    def get_refresh_token(self):
        response = self.token_request()
        return response.json()["refresh"]
