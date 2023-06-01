"""Notion API module."""
import requests

NOTION_VERSION = "2022-02-22"
API_URL = "https://api.notion.com/v1/databases/991958eedf8044eca81f1f4dac5334d2/query"


class NotionAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def retrieve_data(self) -> dict:
        """Retrieve data from Notion API."""
        resp = requests.post(API_URL, headers=self.headers).json()
        return resp["results"]

    @staticmethod
    def get_property(
        result: dict, prop_name: str, prop_type: str, prop_subtype: str
    ) -> str:
        """Get a property from a result."""
        try:
            return result["properties"][prop_name][prop_type][0][prop_subtype]
        except (KeyError, IndexError):
            return None

    @staticmethod
    def get_id(result: dict) -> str:
        """Get the id from a result."""
        return result.get("id")

    @staticmethod
    def get_relation_id(result: dict, prop_name: str) -> list:
        try:
            return [el["id"] for el in result["properties"][prop_name]["relation"]]
        except KeyError:
            return []

    def process_data(self, results: dict) -> list:
        return [
            {
                "title": self.get_property(result, "Name", "title", "plain_text"),
                "id": self.get_id(result),
                "children": self.get_relation_id(result, "Children"),
                "summary": self.get_property(
                    result, "AI summary", "rich_text", "plain_text"
                ),
            }
            for result in results
        ]

    @staticmethod
    def map_id_to_title(data: list) -> dict:
        return {row["id"]: row["title"] for row in data}

    def full_process(self):
        response = self.retrieve_data()
        data = self.process_data(response)
        id_to_title = self.map_id_to_title(data)
        return data, id_to_title
