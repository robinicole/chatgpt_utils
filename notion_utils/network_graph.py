from abc import ABC, abstractmethod
import pandas as pd
import networkx as nx
from pyvis.network import Network
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class NetworkGraph(ABC):
    def __init__(self, data, id_to_title, overlap=-1000):
        self.data = data
        self.id_to_title = id_to_title
        self.overlap = overlap

    @abstractmethod
    def build_graph(self):
        pass

    def save_graph_in_html(self, DG, filename):
        net = Network(notebook=True, directed=False)
        net.from_nx(DG)
        net.force_atlas_2based(overlap=self.overlap)
        net.show(filename)


class NetworkGraphRelation(NetworkGraph):
    def build_graph(self):
        edges = [
            (self.id_to_title[row["id"]], self.id_to_title[child])
            for row in self.data
            for child in row["children"]
            if row["id"] in self.id_to_title and child in self.id_to_title
        ]
        return nx.DiGraph(edges)


class NetworkGraphCorrelation(NetworkGraph):
    def __init__(
        self,
        data,
        id_to_title,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cutoff=0.5,
        overlap=-1000,
    ):
        super().__init__(data, id_to_title, overlap)
        self.cutoff = cutoff
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

    def filter_links(self, links):
        links.columns = ["var1", "var2", "value"]
        return links.loc[
            (links["value"] > self.cutoff) & (links["var1"] != links["var2"])
        ].dropna()

    def build_graph(self):
        links = self.get_links()
        links_filtered = self.filter_links(links)
        return nx.from_pandas_edgelist(links_filtered, "var1", "var2")
