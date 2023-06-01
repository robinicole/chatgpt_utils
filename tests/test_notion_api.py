import unittest
from unittest.mock import patch, MagicMock
from notion_utils.notion_api import NotionAPI  # replace with the actual module name


class TestNotionAPI(unittest.TestCase):
    @patch("notion_utils.notion_api.NotionAPI.list_databases")
    @patch("requests.post")
    def setUp(self, mock_post, mock_list_databases):
        self.mock_post = mock_post
        self.token = "fake_token"
        self.database_name = "fake_database"
        mock_list_databases.return_value = {"fake_database": "fake_id"}
        self.notion_api = NotionAPI(self.token, self.database_name)

    @patch("requests.post")
    def test_retrieve_data(self, mock_post):
        # Success path
        mock_post.return_value.json.return_value = {"results": "fake_results"}
        self.assertEqual(self.notion_api.retrieve_data(), "fake_results")

        # Failure path
        mock_post.return_value.json.side_effect = Exception("API error")
        with self.assertRaises(Exception):
            self.notion_api.retrieve_data()

    @patch("requests.post")
    def test_list_databases(self, mock_post):
        # Success path
        mock_post.return_value.json.return_value = {
            "results": [
                {"title": [{"text": {"content": "fake_database"}}], "id": "fake_id"}
            ]
        }
        self.assertEqual(self.notion_api.list_databases(), {"fake_database": "fake_id"})

        # Failure path
        mock_post.return_value.json.side_effect = Exception("API error")
        with self.assertRaises(Exception):
            self.notion_api.list_databases()

    def test_get_property(self):
        # Assuming 'properties' exists in the result
        result = {
            "properties": {"prop_name": {"prop_type": [{"prop_subtype": "fake_value"}]}}
        }
        self.assertEqual(
            self.notion_api.get_property(
                result, "prop_name", "prop_type", "prop_subtype"
            ),
            "fake_value",
        )

        # Assuming 'properties' does not exist in the result
        result = {}
        self.assertIsNone(
            self.notion_api.get_property(
                result, "prop_name", "prop_type", "prop_subtype"
            )
        )

    def test_get_id(self):
        # Assuming 'id' exists in the result
        result = {"id": "fake_id"}
        self.assertEqual(self.notion_api.get_id(result), "fake_id")

        # Assuming 'id' does not exist in the result
        result = {}
        self.assertIsNone(self.notion_api.get_id(result))

    def test_get_relation_id(self):
        # Assuming 'properties' and 'relation' exist in the result
        result = {"properties": {"prop_name": {"relation": [{"id": "fake_id"}]}}}
        self.assertEqual(
            self.notion_api.get_relation_id(result, "prop_name"), ["fake_id"]
        )

        # Assuming 'properties' or 'relation' does not exist in the result
        result = {}
        self.assertEqual(self.notion_api.get_relation_id(result, "prop_name"), [])

    @patch("notion_utils.notion_api.NotionAPI.get_property")
    @patch("notion_utils.notion_api.NotionAPI.get_id")
    @patch("notion_utils.notion_api.NotionAPI.get_relation_id")
    def test_process_data(self, mock_get_relation_id, mock_get_id, mock_get_property):
        # This test is just for the process_data method itself, and it assumes that the other methods it calls work correctly.
        # We mock these methods so we can control their output and make the test more focused and reliable.
        mock_get_property.return_value = "fake_property"
        mock_get_id.return_value = "fake_id"
        mock_get_relation_id.return_value = ["fake_relation_id"]

        results = [
            {"some_key": "some_value"}
        ]  # The actual content doesn't matter, because we've mocked the methods that would use it.
        processed_data = self.notion_api.process_data(results)
        self.assertEqual(
            processed_data,
            [
                {
                    "title": "fake_property",
                    "id": "fake_id",
                    "children": ["fake_relation_id"],
                    "summary": "fake_property",
                }
            ],
        )

    def test_map_id_to_title(self):
        data = [{"id": "fake_id", "title": "fake_title"}]
        self.assertEqual(
            self.notion_api.map_id_to_title(data), {"fake_id": "fake_title"}
        )

    @patch("notion_utils.notion_api.NotionAPI.retrieve_data")
    @patch("notion_utils.notion_api.NotionAPI.process_data")
    @patch("notion_utils.notion_api.NotionAPI.map_id_to_title")
    def test_full_process(
        self, mock_map_id_to_title, mock_process_data, mock_retrieve_data
    ):
        # Again, we're mocking the methods that full_process calls to make the test more reliable.
        mock_retrieve_data.return_value = "fake_response"
        mock_process_data.return_value = "fake_data"
        mock_map_id_to_title.return_value = "fake_id_to_title"

        data, id_to_title = self.notion_api.full_process()
        self.assertEqual(data, "fake_data")
        self.assertEqual(id_to_title, "fake_id_to_title")


if __name__ == "__main__":
    unittest.main()
