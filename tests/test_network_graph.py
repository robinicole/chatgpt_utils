import unittest
from unittest.mock import MagicMock, patch
from pyvis.network import Network
import networkx as nx
import pandas as pd
from notion_utils.network_graph import (
    NetworkGraphRelation,
    NetworkGraphCorrelation,
)


class TestNetworkGraphRelation(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"id": "id1", "children": ["id2", "id3"]},
            {"id": "id4", "children": ["id1"]},
        ]
        self.id_to_title = {
            "id1": "Title1",
            "id2": "Title2",
            "id3": "Title3",
            "id4": "Title4",
        }
        self.graph_builder = NetworkGraphRelation(self.data, self.id_to_title)

    def test_build_graph(self):
        graph = self.graph_builder.build_graph()
        self.assertEqual(set(graph.nodes), set(self.id_to_title.values()))
        self.assertEqual(
            set(graph.edges),
            {("Title1", "Title2"), ("Title1", "Title3"), ("Title4", "Title1")},
        )


class TestNetworkGraphCorrelation(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"title": "Title1", "summary": "Summary1"},
            {"title": "Title2", "summary": "Summary2"},
        ]
        self.id_to_title = {"id1": "Title1", "id2": "Title2"}
        self.graph_builder = NetworkGraphCorrelation(self.data, self.id_to_title)

    @patch("notion_utils.network_graph.NetworkGraphCorrelation.get_embeddings")
    @patch("notion_utils.network_graph.NetworkGraphCorrelation.get_correlation_matrix")
    @patch("notion_utils.network_graph.NetworkGraphCorrelation.get_links")
    @patch("notion_utils.network_graph.NetworkGraphCorrelation.filter_links")
    def test_build_graph(
        self,
        mock_filter_links,
        mock_get_links,
        mock_get_correlation_matrix,
        mock_get_embeddings,
    ):
        mock_get_links.return_value = MagicMock()
        mock_filter_links.return_value = MagicMock()
        self.graph_builder.build_graph()


class TestNetworkGraphRelationIntegration(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"id": "id1", "children": ["id2", "id3"]},
            {"id": "id4", "children": ["id1"]},
        ]
        self.id_to_title = {
            "id1": "Title1",
            "id2": "Title2",
            "id3": "Title3",
            "id4": "Title4",
        }
        self.graph_builder = NetworkGraphRelation(self.data, self.id_to_title)

    def test_build_graph(self):
        graph = self.graph_builder.build_graph()
        self.assertIsInstance(graph, nx.DiGraph)
        self.assertEqual(set(graph.nodes), set(self.id_to_title.values()))
        self.assertEqual(
            set(graph.edges),
            {("Title1", "Title2"), ("Title1", "Title3"), ("Title4", "Title1")},
        )

    def test_save_graph_in_html(self):
        graph = self.graph_builder.build_graph()
        self.graph_builder.save_graph_in_html(graph, "test_graph.html")
        # Here you would check if the file was created and if it has the correct content.


class TestNetworkGraphCorrelationIntegration(unittest.TestCase):
    def setUp(self):
        self.data = [
            {"title": "Title1", "summary": "Summary1"},
            {"title": "Title2", "summary": "Summary2"},
        ]
        self.id_to_title = {"id1": "Title1", "id2": "Title2"}
        self.graph_builder = NetworkGraphCorrelation(self.data, self.id_to_title)

    def test_get_embeddings(self):
        embeddings = self.graph_builder.get_embeddings()
        # Here you would check the shape and type of the embeddings, and perhaps some properties of the embeddings.

    def test_get_correlation_matrix(self):
        matrix = self.graph_builder.get_correlation_matrix()
        self.assertIsInstance(matrix, pd.DataFrame)
        # Here you would check the shape and values in the correlation matrix, and perhaps some properties of the matrix.

    def test_get_links(self):
        links = self.graph_builder.get_links()
        self.assertIsInstance(links, pd.DataFrame)
        # Here you would check the shape and values in the links DataFrame.

    def test_filter_links(self):
        links = pd.DataFrame(
            {
                "var1": ["Title1", "Title2", "Title1", "Title2"],
                "var2": ["Title2", "Title1", "Title1", "Title2"],
                "value": [0.7, 0.2, 1.0, 0.6],
            }
        )
        filtered_links = self.graph_builder.filter_links(links)
        self.assertIsInstance(filtered_links, pd.DataFrame)
        # Here you would check the shape and values in the filtered_links DataFrame.


if __name__ == "__main__":
    unittest.main()
