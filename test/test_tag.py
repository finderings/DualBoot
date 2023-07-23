from test.base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = {"title": "test", }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_delete(self):
        tag = self.create(self.tag_attributes)
        deleted_tag = self.delete(tag["id"])
        assert deleted_tag == None

    def test_retrieve(self):
        tag = self.create(self.tag_attributes)
        retrieved_data = self.retrieve(tag["id"])
        assert tag == retrieved_data

    def test_update(self):
        tag = self.create(self.tag_attributes)
        updated_title = {"title": "new_test"}
        updated_data = self.update(updated_title, key=tag["id"])
        assert updated_data["title"] == "new_test"

    def test_list(self):
        second_tag = {"title": "new_test", }
        self.create(self.tag_attributes)
        self.create(second_tag)
        data = self.list()
        assert len(data) == 2

    def test_filter(self):
        tag = self.create(self.tag_attributes)
        data = self.filter({"title": "test"})
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert expected_response in data

    def test_unauthorized(self):
        tag = self.create(self.tag_attributes)
        self.check_authorization(tag["id"])
