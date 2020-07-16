import networkx as nx


def get_user_comm(rich_graph, poor_graph, com_type):
    cont = 0
    for node in rich_graph.nodes(data=True):
        poor_graph.nodes[node[0]]['com'] = node[1][com_type]
        poor_graph.nodes[node[0]]['id'] = cont
        cont += 1
    return poor_graph

def create_multi_graph(G, id = 0):
    G_multi = nx.MultiGraph()

    for edge in G.edges(data = True):
        weight = edge[2]['weight']
        for _ in range(int(weight)):
            if edge[0] != edge[1]:
                G_multi.add_edge(edge[0], edge[1])

    if id == 0:           
        G_multi = get_user_comm(G, G_multi, 'weightComm')
    elif id == 1:
        G_multi = get_user_comm(G, G_multi, 'sentimentComm')
    elif id == 2:
        G_multi = get_user_comm(G, G_multi, 'topicComm')
    
    return G_multi