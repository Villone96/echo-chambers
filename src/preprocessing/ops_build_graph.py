from preprocessing.ops_on_raw_data import check_directory_absence
import networkx as nx 
import pandas as pd
import os

def graph_ops():
    garimella_graph()
    covid_graph()
    vax_graph()

def build_garimella_graph(designed_datasets, path, path_data):
    for dataset in designed_datasets: 
        df = pd.read_csv(path_data + '/' + dataset)
        G = nx.Graph()
        [G.add_edge(row[0], row[1] , weight=row[2]) for _, row in df.iterrows()]
        graph_name = dataset.split('_')[2]
        final_G = delete_not_useful_nodes(G)
        nx.write_gml(final_G, path + '/' + graph_name + '.gml')
        final_G.name = graph_name
        print(nx.info(final_G))
        print()

def build_vaccination_graph():
    pass

def build_covid_graph():
    pass

def delete_not_useful_nodes(G):
    node_to_delete = []
    total_edge = 0
    for node in G.nodes():
        for edge in G.edges(node, data = True):
            total_edge += edge[2]['weight']
        if total_edge < 3:
            node_to_delete.append(node)
        total_edge = 0
    
    G.remove_nodes_from(node_to_delete)

    G = G.subgraph(max(nx.connected_components(G)))

    return G

def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data')
    if check_directory_absence('graph', path):
        os.mkdir('Graph')
        os.chdir(os.path.join(path, 'retweet_networks'))

        designed_datasets = ['retweet_graph_ukraine_threshold_largest_CC.txt', 'retweet_graph_gunsense_threshold_largest_CC.txt',
                          'retweet_graph_baltimore_threshold_largest_CC.txt', 'retweet_graph_mothersday_threshold_largest_CC.txt',
                          'retweet_graph_jurassicworld_threshold_largest_CC.txt']

        build_garimella_graph(designed_datasets, os.path.join(path, 'Graph'), os.path.join(path, 'retweet_networks'))

    os.chdir(starting_path)


def covid_graph():
    pass

def vax_graph():
    pass