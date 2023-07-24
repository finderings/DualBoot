from http import HTTPStatus

from test.base import TestViewSetBase

from django.urls import reverse

from freezegun import freeze_time
from datetime import timedelta


class TestJWTAuth(TestViewSetBase):
    any_api_url = reverse("users-list")

    def test_successful_auth(self):
        response = self.token_request()

        assert response.status_code == HTTPStatus.OK
        assert response.json()["refresh"]
        assert response.json()["access"]

    def test_unsuccessful_auth(self):
        response = self.token_request(username="incorrect_username")

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_token_auth(self) -> None:
        client = self.client_class()

        response = client.get(self.any_api_url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

        response = self.token_request()
        token = response.json()["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = client.get(self.any_api_url)

        assert response.status_code == HTTPStatus.OK

    def test_refresh_lives_lower_than_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(hours=23, minutes=59))

            response = self.refresh_token_request(refresh_token)

            assert response.status_code == HTTPStatus.OK
            assert response.json()["access"]

    def test_refresh_dies_after_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(days=1))

            response = self.refresh_token_request(refresh_token)
                    
            assert response.status_code == HTTPStatus.UNAUTHORIZED
