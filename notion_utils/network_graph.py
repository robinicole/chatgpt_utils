"""Module for building network graphs from Notion data."""
from abc import ABC, abstractmethod
import pandas as pd
import networkx as nx
from pyvis.network import Network
from sklearn.metrics.pairwise import cosine_similarity


class GraphBuilder(ABC):
    def __init__(self, data, id_to_title):
        self.data = data
        self.id_to_title = id_to_title

    @abstractmethod
    def build_graph(self, **kwargs):
        pass

    def save_graph_in_html(self, DG, filename, overlap=-1000):
        net = Network(notebook=True, directed=False)
        net.from_nx(DG)
        net.force_atlas_2based(overlap=overlap)
        net.show(filename)


class NetworkGraphRelation(GraphBuilder):
    name: str = "relations_graph"

    def build_graph(self, **kwargs):
        edges = [
            (self.id_to_title[row["id"]], self.id_to_title[child])
            for row in self.data
            for child in row["children"]
            if row["id"] in self.id_to_title and child in self.id_to_title
        ]
        return nx.DiGraph(edges)


class NetworkGraphCorrelation(GraphBuilder):
    name: str = "correlations_graph"

    def __init__(
        self,
        data,
        id_to_title,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    ):
        from sentence_transformers import SentenceTransformer

        super().__init__(data, id_to_title)
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self):
        title_summary = [f"{el['title']}{el['summary']}" for el in self.data]
        return self.model.encode(title_summary, convert_to_tensor=True)

    def get_correlation_matrix(self):
        embeddings = self.get_embeddings()
        cosine_sim_matrix = cosine_similarity(embeddings)
        titles = [el["title"] for el in self.data]
        return pd.DataFrame(cosine_sim_matrix, columns=titles, index=titles)

    def get_links(self):
        correlation_matrix = self.get_correlation_matrix()
        return correlation_matrix.stack().reset_index()

    def filter_links(self, links, cutoff=0.5):
        links.columns = ["var1", "var2", "value"]
        return links.loc[
            (links["value"] > cutoff) & (links["var1"] != links["var2"])
        ].dropna()

    def build_graph(self, **kwargs):
        cutoff = kwargs.get("cutoff", 0.5)
        links = self.get_links()
        links_filtered = self.filter_links(links, cutoff=cutoff)
        return nx.from_pandas_edgelist(links_filtered, "var1", "var2")
