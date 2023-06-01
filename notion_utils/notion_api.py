"""Notion API module."""
import requests

NOTION_VERSION = "2022-02-22"
API_URL = "https://api.notion.com/v1/databases/{database_id}/query"


class NotionAPI:
    def __init__(self, token, datatabase_name):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }
        try:
            database_id = self.list_databases()[datatabase_name]
        except KeyError:
            print("Database not found")
        self.api_url = API_URL.format(database_id=database_id)

    def retrieve_data(self) -> dict:
        """Retrieve data from Notion API."""
        resp = requests.post(self.api_url, headers=self.headers).json()
        return resp["results"]

    def list_databases(self):
        objs = requests.post(
            "https://api.notion.com/v1/search",
            json={
                "filter": {
                    "value": "database",
                    "property": "object",
                },
            },
            headers=self.headers,
        )
        objs = objs.json()["results"]
        db_to_id = dict()
        for obj in objs:
            try:
                db_to_id[obj["title"][0]["text"]["content"]] = obj["id"]
            except:
                pass
        return db_to_id

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

    def process_data(self, results: dict, children_name="Children") -> list:
        return [
            {
                "title": self.get_property(result, "Name", "title", "plain_text"),
                "id": self.get_id(result),
                "children": self.get_relation_id(result, children_name),
                "summary": self.get_property(
                    result, "AI summary", "rich_text", "plain_text"
                ),
            }
            for result in results
        ]

    @staticmethod
    def map_id_to_title(data: list) -> dict:
        return {row["id"]: row["title"] for row in data}

    def full_process(self, children_name="Children"):
        response = self.retrieve_data()
        data = self.process_data(response, children_name)
        id_to_title = self.map_id_to_title(data)
        return data, id_to_title
