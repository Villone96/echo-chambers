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



def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data')
    if check_directory_absence('graph', path):
        # os.mkdir('Graph')
        os.chdir(os.path.join(path, 'retweet_networks'))

        designed_datasets = ['retweet_graph_ukraine_threshold_largest_CC.txt', 'retweet_graph_gunsense_threshold_largest_CC.txt',
                          'retweet_graph_baltimore_threshold_largest_CC.txt', 'retweet_graph_mothersday_threshold_largest_CC.txt',
                          'retweet_graph_nationalkissingday_threshold_largest_CC.txt']

        build_garimella_graph(designed_datasets, path, os.path.join(path, 'retweet_networks'))

        


    os.chdir(starting_path)


def covid_graph():
    pass

def vax_graph():
    pass