import networkx as nx

def nx_to_cyto(graph: nx.Graph, positions=None) -> tuple[list, list]:

    if not positions:
        positions = nx.spring_layout(graph)
    else:
        assert isinstance(positions, dict), "positions needs to be a dict with the node positions"


    node_data = [{"data": {"id": str(i), "label": str(i)}, 
                "position": {"x": positions[i][0]*100, "y": positions[i][1]*100}, 
                # "locked":False,
                # "style": {"shape": "circle",
                #             'width': 30,
                #             'height': 30,
                #             "color": "white",
                #             }
                } 
                for i in list(graph.nodes())]

    edge_data = [{'data': {'source': str(i[0]), 'target': str(i[1])}} for i in graph.edges()]
              # "style": {'line-color': '#9e9e26', # 
              #           'width': 2}} 


    return node_data, edge_data
