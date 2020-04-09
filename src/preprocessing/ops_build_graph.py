from preprocessing.ops_on_raw_data import check_directory_absence
import networkx as nx 
import pandas as pd
import os
import ast

def graph_ops():
    garimella_graph()
    covid_graph()
    vax_graph()

def delete_not_useful_nodes_garimella(G):
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

def build_garimella_graph(designed_datasets, path):
    for dataset in designed_datasets: 
        df = pd.read_csv(dataset)
        G = nx.Graph()
        [G.add_edge(row[0], row[1] , weight=row[2]) for _, row in df.iterrows()]
        graph_name = dataset.split('_')[2]
        G.name = graph_name
        print(nx.info(G))
        print()
        final_G = delete_not_useful_nodes_garimella(G)
        nx.write_gml(final_G, path + '/' + graph_name + '.gml')
        final_G.name = graph_name
        print(nx.info(final_G))
        print('-----------------------------------------------')

def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data')
    if check_directory_absence('Graph', path):
        os.mkdir('Graph')
        os.chdir(os.path.join(path, 'retweet_networks'))

        designed_datasets = ['retweet_graph_ukraine_threshold_largest_CC.txt', 'retweet_graph_gunsense_threshold_largest_CC.txt',
                          'retweet_graph_baltimore_threshold_largest_CC.txt', 'retweet_graph_mothersday_threshold_largest_CC.txt',
                          'retweet_graph_jurassicworld_threshold_largest_CC.txt']

        build_garimella_graph(designed_datasets, os.path.join(path, 'Graph'))

    os.chdir(starting_path)

def build_covid_graph():
    pass

def covid_graph():
    pass

def remove_not_usefull_node_vaccination(G):
    node_to_delete = []
    for node in G.nodes():
        if G.degree[node] < 3:
            node_to_delete.append(node)

    G.remove_nodes_from(node_to_delete)

    G = G.subgraph(max(nx.connected_components(G)))

    G.name = 'Final Vaccination Graph'

    return G

def add_edge(G, row, source, destination):

    if G.has_edge(source, destination):
        tweets = list(G[source][destination]['tweets'])
        tweets.append(row[2]) 
        hastags = list(G[source][destination]['hashtags'])
        hastags.append(row[7]) 


        G[source][destination]['tweets'].append(row[2])
        G[source][destination]['hashtags'].append(row[7])

    else:
        G.add_edge(source, destination, tweets=[row[2]], hashtags=[row[7]])

    return G


def build_vaccination_graph(path):
    df = pd.read_csv(path + '/final_data/' + 'Final_data.csv', lineterminator='\n')
    G = nx.Graph()
    num_edge = 0
    num_nodes = 0
    for _, row in df.iterrows():
        num_nodes += 1
        mentions = ast.literal_eval(row[3])
        if 'self' in mentions:
            G = add_edge(G, row, row[1], row[1], num_edge)
        else:
            for mention in mentions:
                G = add_edge(G, row, row[1], mention, num_edge)


    G.name = 'Started Vaccination Graph'
    print(nx.info(G))

    final_G = remove_not_usefull_node_vaccination(G)

    print()
    print(nx.info(final_G))
    print('---------------------------------------')
    nx.write_gml(final_G, path + '/Graph/vaccination.gml')


def vax_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax')
    if check_directory_absence('Graph', path):
        os.mkdir('Graph')
        os.chdir(os.path.join(path, 'final_data'))
        build_vaccination_graph(path)

    os.chdir(starting_path)
