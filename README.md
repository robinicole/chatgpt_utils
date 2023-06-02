# Python Notion API and Network Graph Library

This library provides a Python interface for interacting with the Notion API to extract data from databases and visualize it as network graphs. It includes two main modules: `notion_api.py` and `network_graph.py`.

## `notion_api.py`

This module defines the `NotionAPI` class, which is used to interact with the Notion API.

The class's methods include:

- `retrieve_data`: Retrieve data from a specified Notion database.
- `list_databases`: List all databases available.
- `get_property`: Extract a property from a given result.
- `get_id`: Get the id from a given result.
- `get_relation_id`: Get the ids of related items from a given result.
- `process_data`: Process the retrieved data for easier handling.
- `map_id_to_title`: Map ids to titles for easy reference.
- `full_process`: Execute a full data retrieval and processing pipeline.

## `network_graph.py`

This module defines abstract and concrete classes for creating network graphs from the data retrieved from Notion.

The main classes include:

- `NetworkGraph`: This is an abstract base class that sets the basic structure for network graph classes.
- `NetworkGraphRelation`: This class builds a network graph based on relations between items.
- `NetworkGraphCorrelation`: This class builds a network graph based on cosine similarity between text summaries of items.

Both concrete classes include a method `build_graph` for constructing the graph and a method `save_graph_in_html` for visualizing and saving the graph in HTML format.

## Requirements

The following Python packages are used:

- `requests` for sending HTTP requests.
- `networkx` and `pyvis` for creating and visualizing network graphs.
- `sentence_transformers` and `sklearn` for text embeddings and cosine similarity computation.
- `pandas` for handling data.

## Usage

To use these modules, you first need to create an instance of `NotionAPI` and provide your Notion API token and the name of the database you want to work with. After retrieving and processing the data, you can then create a `NetworkGraphRelation` or `NetworkGraphCorrelation` object and call its `build_graph` and `save_graph_in_html` methods.

## Example

```python
from notion_utils.notion_api import NotionAPI
from notion_utils.network_graph import NetworkGraphRelation, NetworkGraphCorrelation

# Notion API token and database name
token = "YOUR_NOTION_API_TOKEN"
database_name = "DATABASE_NAME"

# Create Notion API object and retrieve data
notion_api = NotionAPI(token, database_name)
data, id_to_title = notion_api.full_process()

# Create network graph
graph_relation = NetworkGraphRelation(data, id_to_title)
graph_relation.build_graph()
graph_relation.save_graph_in_html("relation_graph.html")

graph_correlation = NetworkGraphCorrelation(data, id_to_title)
graph_correlation.build_graph()
graph_correlation.save_graph_in_html("correlation_graph.html")
```

Replace `"YOUR_NOTION_API_TOKEN"` and `"DATABASE_NAME"` with your actual Notion API token and the name of your Notion database. This example creates two types of graphs: one based on relations between items and another based on cosine similarity of their summaries. Both graphs are then saved as HTML files.

Remember to install all the necessary packages before running the code:

```bash
pip install requests networkx pyvis pandas sentence-transformers sklearn
```

## Disclaimer

This is not an official Notion product. It is an open-source project developed to provide a Python interface for the Notion API.
