import os
import random
import networkx as nx

def start_link_opt():
    garimella()
    covid()
    vaccination()


def garimella():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data/Graph')
    os.chdir(path)
    list_of_graph = os.listdir(path)
    for graph in list_of_graph:
        name = graph
        if 'Multi' in name: 
            continue
        else:
            print(name)
            name = name.split('.')[0]
            graph = nx.read_gml(f'{name}.gml')
    os.chdir(starting_path)

def covid():
    pass

def vaccination():
    pass