from test.base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = {"title": "test"}
    another_tag_attributes = {"title": "new_title"}

    def setUp(self) -> None:
        super().setUp()
        self.tag = self.create(self.tag_attributes)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        expected_response = self.expected_details(
            self.tag, self.tag_attributes
            )

        assert self.tag == expected_response

    def test_delete(self):
        deleted_tag = self.delete(self.tag["id"])

        assert deleted_tag == None

    def test_retrieve(self):
        retrieved_data = self.retrieve(self.tag["id"])

        assert self.tag == retrieved_data

    def test_update(self):
        updated_data = self.update(
            self.another_tag_attributes, key=self.tag["id"]
            )

        assert updated_data["title"] == "new_title"

    def test_list(self):
        self.create(self.another_tag_attributes)

        data = self.list()

        assert len(data) == 2

    def test_filter(self):
        wrong_tag = self.create(self.another_tag_attributes)
        data = self.filter({"title": "test"})

        expected_response_match = self.expected_details(
            self.tag, self.tag_attributes
            )
        expected_response_no_match = self.expected_details(
            wrong_tag, self.another_tag_attributes
            )

        assert expected_response_match in data
        assert expected_response_no_match not in data

    def test_unauthorized(self):
        self.check_authorization(self.tag["id"])
