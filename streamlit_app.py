import streamlit as st
from notion_utils.notion_api import NotionAPI, list_databases
from notion_utils.network_graph import NetworkGraphCorrelation, NetworkGraphRelation
import streamlit.components.v1 as components
import os

AVAILABLE_GRAPHS = [NetworkGraphRelation, NetworkGraphCorrelation]
GRAPHS_DICT = {gr.name: gr for gr in AVAILABLE_GRAPHS}

# Title of the app
st.title("Notion Notes Graph Drawer")

# Input fields for various parameters
token = st.text_input("Enter your Notion token:", type="password")


@st.cache
def list_databases_with_relations(token):
    databases = list_databases(token)
    databases_with_relations = {}
    for db_name, db_info in databases.items():
        if db_info["self_relation_properties"]:
            databases_with_relations[db_name] = db_info
    return databases_with_relations


@st.cache
def get_notion_data(token, database_name):
    return NotionAPI(token, database_name)


if token:
    try:
        databases = list_databases_with_relations(token)
        database_name = st.selectbox("Select a Notion database:", databases)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    cutoff = st.slider(
        "Select correlation cutoff:", min_value=0.0, max_value=1.0, value=0.5, step=0.1
    )
    overlap = st.number_input(
        "Enter overlap for force atlas 2 based:", value=-1000, step=100
    )
    graph_kind = st.selectbox("Select a graph kind to draw:", list(GRAPHS_DICT.keys()))
    children_name = st.selectbox(
        "Name of the children property in Notion:",
        list(databases[database_name]["self_relation_properties"]),
    )
    # Button to trigger the graph drawing
    if st.button("Draw Graph"):
        if not token or not database_name:
            st.warning("Please enter a Notion token and select a database.")
        else:
            try:
                # Get data from Notion API
                notion_api = get_notion_data(token, database_name)
                data, id_to_title = notion_api.full_process(children_name)
                # Build and display graph
                GraphBuilder = GRAPHS_DICT[graph_kind]
                network_graph = GraphBuilder(data, id_to_title)
                graph = network_graph.build_graph(cutoff=cutoff)
                network_graph.save_graph_in_html(graph, "tmp.html", overlap=overlap)
                HtmlFile = open("tmp.html", "r", encoding="utf-8")
                source_code = HtmlFile.read()
                components.html(source_code, height=600 * 2, width=800 * 2)
                # components.iframe("./tmp.html")
            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.warning("Please enter your Notion token to list databases and draw graphs.")
