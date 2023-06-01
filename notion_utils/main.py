import argparse
from pyvis.network import Network
from notion_utils.notion_api import NotionAPI
from notion_utils.network_graph import NetworkGraphCorrelation, NetworkGraphRelation


def main():
    parser = argparse.ArgumentParser(description="Draw a notes graph from Notion")
    parser.add_argument("--token", required=True, help="Your Notion token")
    parser.add_argument(
        "--cutoff",
        type=float,
        default=0.5,
        help="Correlation cutoff for when we draw the graph with the correlation matrix",
    )
    parser.add_argument(
        "--overlap", type=int, default=-1000, help="Overlap for force atlas 2based"
    )
    parser.add_argument(
        "--graph_kinds",
        nargs="+",
        default=["relations", "correlations"],
        help="Graph kinds to draw, it can be one of relations or correlations",
    )
    args = parser.parse_args()

    # Get data from Notion API
    notion_api = NotionAPI(args.token)
    data, id_to_title = notion_api.full_process()

    # Build and display graph
    for GraphBuilder, output, kind in zip(
        [NetworkGraphRelation, NetworkGraphCorrelation],
        ["graph_relations.html", "graph_correlations.html"],
        ["relations", "correlations"],
    ):
        if kind in args.graph_kinds:
            network_graph = GraphBuilder(data, id_to_title)
            graph = network_graph.build_graph()
            print(f"Saving {kind} graph in {output}")
            network_graph.save_graph_in_html(graph, output)


if __name__ == "__main__":
    main()
