from ast import literal_eval
import networkx as nx
import pandas as pd
import numpy as np
import plotly.express as px
from plot_graph import nx_to_cyto
import dash
import dash_cytoscape as cyto  
from dash import dcc, html
from dash.dependencies import Output, Input, State
import pandas as pd  
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import os
import dash_mantine_components as dmc




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder="assets/")
all_words = pd.read_csv("data/words.csv")
all_chars = pd.read_csv("data/chars.csv")


def generate_edges(word_components: list[str], meaning):
    edges = []
    edges_nx = []
    for idx in range(len(word_components)-1):
        # {'data': {'source': str(i[0]), 'target': str(i[1])}} for i in graph.edges()]
        
        edges_nx.append((word_components[idx], word_components[idx+1]))
        edges.append({
            "data": {
                "source": word_components[idx], 
                "target": word_components[idx+1],
                "meaning": meaning[0] if len(meaning) != 0 else ""
            },
            "classes": f"word_length_{len(word_components)}"
            }
        )
    return edges, edges_nx


def filter_graph_hanzi(df:pd.DataFrame, char:str):
    return df.loc[df["characters"].str.contains(char)]


def filter_graph_word(df:pd.DataFrame, word:str):
    return df.loc[df["meanings"].str.contains(word)]


def filter_hsk(df:pd.DataFrame, level:str):
    raise NotImplementedError


def gen_graph(df, pos_scaling=10000):
    edge_set = []
    edges_nx_all = []

    char_pinyin_mapping = dict(zip(all_chars["character"], all_chars["pinyin"]))


    for word in df.to_dict("records"):
        edges, edges_nx = generate_edges(literal_eval(word["characters"]), literal_eval(word["meanings"]))
        edge_set += edges
        edges_nx_all += edges_nx

    g = nx.Graph(edges_nx_all)
    positions = nx.spring_layout(g)

    node_set = [{"data": {"id": str(i), "label": str(i)+char_pinyin_mapping.get(i, "")}, 
                    "position": {"x": positions[i][0]*pos_scaling, "y": positions[i][1]*pos_scaling}, 
                    # "locked":False,
                    # "style": {"shape": "circle",
                    #             'width': 30,
                    #             'height': 30,
                    #             "color": "white",
                    #             }
                    } 
                    for i in list(g.nodes())]
    
    # rint(node_set)
    
    return node_set, edge_set


node_set, edge_set = gen_graph(all_words)

app.layout = html.Div([
    dmc.Grid([
        dmc.Col([
            dmc.TextInput(label="Search for Character", id="search-character"),
        ], span=6),
        dmc.Col([
            dmc.Button("Search", id="search-btn")
        ], span=2),
        dmc.Col([
            dmc.Select(
            label="Filter by HSK level",
            placeholder="Select Multiple",
            id="hsk-select",
            value="ng",
            data=[{"value": "HSK"+str(i), "label": "HSK"+str(i)} for i in range(1,6)],
            # style={"width": 200, "marginBottom": 10},
        ),
        ], span=4)
    ], style={"margin":"1%"}, align="flex-end"),
    dbc.Row([
        cyto.Cytoscape(
        id='graph',
        layout={'name': 'preset'},
        style={
            'width': '100%', 
            'height': '800px',
        },
        elements=[
            *node_set,
            *edge_set
        ],
        stylesheet=[
        # Group selectors
        { # https://js.cytoscape.org/#style/node-body
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-halign':'center',
                'text-valign':'center',
                # 'background-color':"red"
                # 'width':'label',
                # 'height':'label',v
                # 'shape':'square'
            }
        },
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                # 'text-halign':'center',
                # 'text-valign':'center',
                'border-width':"2px"
                # 'background-color':"red"
                # 'width':'label',
                # 'height':'label',
                # 'shape':'square'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-color': 'red',
                'target-arrow-shape': 'triangle',
                'label': 'data(meaning)',
                "text-background-color":"blue",
                "text-background-shape":"rectangle",
                "text-outline-color":"red",
                "text-rotation":"autorotate",
                "text-margin-y":"0px",
                "text-margin-x":"0px",
                "line-width":"10px"

        #         'line-color': 'red'
            }
        },
        {
            'selector': '.word_length_2',
            'style': {
                'line-color': '#c6b4ee'
            },
        },
        {
            'selector': '.word_length_3',
            'style': {
                'line-color': '#99ffcc'
            }
        },
        {
            'selector': '.word_length_4',
            'style': {
                'line-color': 'yellow'
            }
        },
        {
            'selector': '.word_length_4',
            'style': {
                'line-color': '#cce6ff'
            }
        }
        
        
        ],
    )
    ], class_name="graph-component")

])



@app.callback(
    Output("graph", "elements"),
    State("search-character", "value"),
    Input("search-btn", "n_clicks"),
)

def update_graph(search_string:str, n_clicks:int):
    print(search_string)
    if n_clicks and search_string!="" and search_string:

        # if search_string.isalnum():
        #     print("alnum search")
        #     df = filter_graph_word(all_words, search_string)
        # else:
        #     print("hanzi search")
        df = filter_graph_hanzi(all_words, search_string)


        node_set, edge_set = gen_graph(df, 1000)
        return [*node_set, *edge_set]
    else:
        node_set, edge_set = gen_graph(all_words)
        return [*node_set, *edge_set]



if __name__ == "__main__":
    app.run_server(debug=True)