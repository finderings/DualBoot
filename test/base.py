from http import HTTPStatus
from typing import List, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.admin = cls.create_api_admin()
        cls.client = APIClient()

    def setUp(self) -> None:
        self.client.force_login(self.admin)

    @classmethod
    def create_api_user(cls):
        return User.objects.create(username="user@test.ru")

    @classmethod
    def create_api_admin(cls):
        return User.objects.create_superuser(
            "admin@test.ru", email=None, password=None
            )

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
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data
