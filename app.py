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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


edges = [("广", "东"), ("广", "宽")]
# edges = [(1,2), (1,3)]
g = nx.Graph(edges)
node_data, edge_data = nx_to_cyto(g)


print(node_data, edge_data)


app.layout = html.Div([
    dbc.Row([
        html.Div("Hello")
    ]),
    dbc.Row([
        cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={
            'width': '100%', 
            'height': '800px',
        },
        elements=[
            *node_data,
            *edge_data
        ],
        stylesheet=[
        # Group selectors
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-halign':'center',
                'text-valign':'center',
                # 'width':'label',
                # 'height':'label',
                # 'shape':'square'
            }
        },]
        # stylesheet=[{
        #     'selector': 'edge',
        #     'style': {
        #         'curve-style': 'bezier',
        #         'source-arrow-color': 'red',
        #         'source-arrow-shape': 'triangle',
        #         'line-color': 'red'
        #     }
        # }],
    )
    ])

])

if __name__ == "__main__":
    app.run_server(debug=True)