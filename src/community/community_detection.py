import igraph as ig
import networkx as nx
from networkx.algorithms.community.quality import coverage 
import os
from tqdm import tqdm
import time
import logging

def start_community_detection():
    garimella_graph()
    covid_graph()
    vax_graph()

def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data/Graph')
    os.chdir(path)
    list_of_graph = os.listdir(path)
    logging.basicConfig(filename='Garimella_logfile.log', level=logging.INFO, format='%(asctime)s:%(message)s')
    for graph in list_of_graph:
        name = graph
        if 'Multi' in name or 'mothers' in name: 
            pass
        else:
            print(f'{name} graph')
            graph = nx.read_gml(f'{name}')
            multi = nx.read_gml(f'Multi_{name}')
            print(nx.info(graph))
            print(nx.info(multi))
            print()
            graph_info = f'\nGraph Info\n{nx.info(graph)}\nMulti graph Info\n{nx.info(multi)}\n\n\n'
            logging.info(graph_info)

            





    os.chdir(starting_path)



def covid_graph():
    pass

def vax_graph():
    pass
    