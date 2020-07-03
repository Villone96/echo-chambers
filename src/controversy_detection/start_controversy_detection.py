import os

import random
from controversy_detection.random_walks import random_walks, random_walks_centrality
from controversy_detection.GMCK import start_GMCK
from controversy_detection.EC import start_EC
import logging
from datetime import datetime
import networkx as nx
from controversy_detection.log_writer import log_write_start_end


def start_detection():
    logging.basicConfig(filename='controversy_detection.log', level=logging.INFO, format='%(message)s')
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f'RUN TIME: {today}')
    #garimella_graph()
    covid_graph()
    vax_graph()


def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data/Graph')
    os.chdir(path)
    list_of_graph = os.listdir(path)
    log_write_start_end(True, 'GARIMELLA GRAPH')
    for graph in list_of_graph:
        name = graph
        if 'Multi' in name: 
            continue
        else:
            print(name)
            name = name.split('.')[0]
            graph = nx.read_gml(f'{name}.gml')

            logging.info(f'Graph: {name}')
            random_walks(graph, 0.6, 200)
            random_walks_centrality(graph)
            print()

            start_GMCK(graph, 'weightComm')
            print()

            start_EC(graph, 'weightComm')
            print()
    os.chdir(starting_path)
    log_write_start_end(False)

def covid_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus/Graph')
    os.chdir(path)
    log_write_start_end(True, 'CORONA VIRUS')
    graph = nx.read_gml('Final_Graph_Covid.gml')

    random_walks(graph, 0.6, 200)
    random_walks_centrality(graph)
    print()

    start_GMCK(graph, 'weightComm')
    print()

    start_EC(graph, 'weightComm')
    print()
    os.chdir(starting_path)
    log_write_start_end(False)

def vax_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax/Graph')
    os.chdir(path)
    log_write_start_end(True, 'Vaccination')
    graph = nx.read_gml('Final_Graph_Vax.gml')

    random_walks(graph, 0.6, 200)
    random_walks_centrality(graph)
    print()

    start_GMCK(graph, 'weightComm')
    print()

    start_EC(graph, 'weightComm')
    print()
    os.chdir(starting_path)
    log_write_start_end(False)