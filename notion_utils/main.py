"""Main module to draw a notes graph from Notion."""
import typer
from typing import List
from notion_utils.notion_api import NotionAPI, list_databases
from notion_utils.network_graph import NetworkGraphCorrelation, NetworkGraphRelation

app = typer.Typer()

AVAILABLE_GRAPHS = [NetworkGraphRelation, NetworkGraphCorrelation]
AVAILABLE_GRAPHS_NAMES = [gr.name for gr in AVAILABLE_GRAPHS]
GRAPH_NAMES_STRING = ", ".join(AVAILABLE_GRAPHS_NAMES)


@app.command("draw_graph")
def main(
    token: str = typer.Option(..., help="Your Notion token"),
    cutoff: float = typer.Option(
        0.5,
        help="Correlation cutoff for when we draw the graph with the correlation matrix",
    ),
    overlap: int = typer.Option(-1000, help="Overlap for force atlas 2 based"),
    graph_kinds: str = typer.Option(
        GRAPH_NAMES_STRING,
        help=f"Graph kinds to draw, it can be one of {GRAPH_NAMES_STRING}",
    ),
    children_name: str = typer.Option(
        "Child Task", help="Name of the children property in Notion"
    ),
    database_name: str = typer.Option("GTD Tasks", help="Notion database"),
    file_prefix: str = typer.Option("", help="Prefix for the output files"),
):
    graph_kinds = graph_kinds.split(",")
    for input_graph_name in graph_kinds:
        if input_graph_name not in AVAILABLE_GRAPHS_NAMES:
            raise ValueError(
                f"Graph name {input_graph_name} not in {AVAILABLE_GRAPHS_NAMES}"
            )
    print(graph_kinds)
    # Get data from Notion API
    notion_api = NotionAPI(token, database_name)
    data, id_to_title = notion_api.full_process(children_name)

    # Build and display graph
    for GraphBuilder in AVAILABLE_GRAPHS:
        name = GraphBuilder.name
        if name in graph_kinds:
            filename = f"{file_prefix}_{name}.html"
            network_graph = GraphBuilder(data, id_to_title)
            graph = network_graph.build_graph(cutoff=cutoff)
            typer.echo(f"Saving {name} graph in {filename}")
            network_graph.save_graph_in_html(graph, filename, overlap=overlap)


@app.command("list-databases")
def list_databases_command(token: str = typer.Option(..., help="Your Notion token")):
    # TODO : make it work
    databases = list_databases(token)
    for key, val in databases.items():
        if val["self_relation_properties"]:
            typer.echo(f"{key} : {val}")


if __name__ == "__main__":
    app()
