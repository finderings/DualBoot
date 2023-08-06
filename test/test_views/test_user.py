from test.base import TestViewSetBase
from test.fixtures.factories.user import UserFactory

from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile

import factory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
     
    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes,
                "id": entity["id"],
                "phone": entity["phone"],
                "avatar_picture": entity["avatar_picture"],
                }

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)

        expected_response = self.expected_details(
            user, user_attributes
            )

        assert user == expected_response

    def test_delete(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)

        deleted_user = self.delete(user["id"])

        assert deleted_user == None

    def test_retrieve(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        del user['phone']
        
        retrieved_data = self.retrieve(user, user["id"])
        del retrieved_data['phone']

        assert user == retrieved_data

    def test_update(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        another_user_attributes = factory.build(
            dict, FACTORY_CLASS=UserFactory
            )
        user = self.create(user_attributes)
        user_attributes["first_name"] = "Johnny"
        another_user_attributes["first_name"] = "Jimmy"

        updated_user = self.update(
            another_user_attributes, key=user["id"]
            )
        expected_response = self.expected_details(
            user, user_attributes
            )
        
        expected_response["avatar_picture"] = updated_user["avatar_picture"]

        assert updated_user["first_name"] == "Jimmy"
        assert expected_response["avatar_picture"] == updated_user[
            "avatar_picture"
            ]

    def test_list(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.create(user_attributes)
        data = self.list()

        assert len(data) == 1

    def test_filter(self):
        user_attributes = factory.build(
            dict, FACTORY_CLASS=UserFactory, first_name="Johnny"
            )
        another_user_attributes = factory.build(
            dict, FACTORY_CLASS=UserFactory, first_name="Jimmy"
            )
        user = self.create(user_attributes)
        
        data = self.list({"first_name": "John"})

        expected_response_match = self.expected_details(
            user, user_attributes
            )
        expected_response_no_match = self.expected_details(
            user, another_user_attributes
            )

        assert expected_response_match in data
        assert expected_response_no_match not in data

    def test_unauthorized(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        self.check_authorization(user["id"])

    def test_large_avatar(self) -> None:
        avatar_file = SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        user_attributes = factory.build(
            dict, FACTORY_CLASS=UserFactory, avatar_picture=avatar_file
            )

        response = self.request_create(user_attributes)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": ["Maximum size 1048576 exceeded."]
            }

    def test_avatar_bad_extension(self) -> None:
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"

        response = self.request_create(user_attributes)
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
