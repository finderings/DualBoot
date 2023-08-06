from http import HTTPStatus
from typing import List, Union

from requests import Response

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .fixtures.factories.user import SuperUserFactory


class TestViewSetBase(APITestCase):
    user: SuperUserFactory = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = cls.create_api_admin()
        cls.client = APIClient()

    def setUp(self) -> None:
        super().setUp()
        self.client.force_authenticate(user=self.admin)

    @classmethod
    def create_api_admin(cls):
        return SuperUserFactory.build()

    @classmethod
    def detail_url(
        cls, key: Union[Union[int, str], List[Union[int, str]]]
    ) -> str:
        return reverse(f"{cls.basename}-detail",
                       args=key if isinstance(key, list) else [key]
                       )

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def request_create(
        self, data: dict, args: List[Union[str, int]] = None
    ) -> Response:
        url = self.list_url(args)
        return self.client.post(url, data=data)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.request_create(data, args)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_list(
        self, data: dict = None, args: List[Union[str, int]] = None
    ) -> Response:
        url = self.list_url(args)
        return self.client.get(url, data=data)

    def list(
            self, data: dict = None, args: List[Union[str, int]] = None
            ) -> dict:
        response = self.request_list(data, args)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_retrieve(
        self,
        data: dict = None,
        key: Union[Union[int, str], List[Union[int, str]]] = None
    ) -> Response:
        url = self.detail_url(key)
        return self.client.get(url, data=data)

    def retrieve(self,
                 data: dict,
                 key: Union[Union[int, str], List[Union[int, str]]] = None
                 ) -> dict:
        response = self.request_retrieve(data, key=key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_update(self,
                       data: dict = None,
                       key: Union[Union[int, str], List[Union[int, str]]] = None
                       ) -> Response:
        url = self.detail_url(key)
        return self.client.put(url, data=data)

    def update(self,
               data: dict = None,
               key: Union[Union[int, str], List[Union[int, str]]] = None
               ) -> dict:
        response = self.request_update(data, key)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def request_delete(
            self, key: Union[Union[int, str], List[Union[int, str]]]
            ) -> Response:
        url = self.detail_url(key)
        return self.client.delete(url)

    def delete(
            self, key: Union[Union[int, str], List[Union[int, str]]]
            ) -> None:
        response = self.request_delete(key)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response.data

    def check_authorization(self, key: Union[str, int]) -> None:
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        return response.data

    def request_single_resource(self, data: dict = None) -> Response:
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
