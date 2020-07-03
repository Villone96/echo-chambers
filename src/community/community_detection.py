import os
from tqdm import tqdm
from datetime import datetime
import logging

from community.com_utilities import community_detection, note_difference
from community.log_writer import log_write_start_end


def start_community_detection():
    files = os.listdir(os.getcwd())
    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f'RUN TIME: {today}')
    garimella_graph()
    covid_graph()
    vax_graph()

def garimella_graph():
    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data/Graph')
    os.chdir(path)
    list_of_graph = os.listdir(path)
    log_write_start_end(True, 'GARIMELLA GRAPH')
    for graph in list_of_graph:
        name = graph
        if 'Multi' in name: 
            pass
        else:
            print(name)
            logging.info(f'GRAPH NAME: {name}')
            name = name.split('.')[0]
            community_detection(name, 0, 'weight')

    os.chdir(starting_path)
    log_write_start_end(False)


def covid_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus/Graph')
    os.chdir(path)             
    log_write_start_end(True, 'COVID-19 GRAPH')

    info_no_sent_metis, info_no_sent_fluid = community_detection('Covid', 1, 'weight')
    info_sent_metis, info_sent_fluid = community_detection('Covid', 1, 'sentiment')
    info_topic_metis, info_topic_fluid = community_detection('Covid', 1, 'topic')
    info_hybrid_metis, info_hybrid_fluid = community_detection('Covid', 1, 'hybrid')

    note_difference(info_no_sent_metis, info_sent_metis, 'Metis', 'sentiment')
    note_difference(info_no_sent_metis, info_topic_metis, 'Metis', 'topic')
    note_difference(info_no_sent_metis, info_hybrid_metis, 'Metis', 'hybrid')

    # note_difference(info_no_sent_fluid, info_sent_fluid, 'Fluid')

    os.chdir(starting_path)
    log_write_start_end(False, 'Covid')


def vax_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax/Graph')
    os.chdir(path)             
    log_write_start_end(True, 'VACCINATION GRAPH')
    info_no_sent_metis, info_no_sent_fluid = community_detection('Vax', 1, 'weight')
    info_sent_metis, info_sent_fluid = community_detection('Vax', 1, 'sentiment')
    info_topic_metis, info_topic_fluid = community_detection('Vax', 1, 'topic')
    info_hybrid_metis, info_hybrid_fluid = community_detection('Vax', 1, 'hybrid')

    note_difference(info_no_sent_metis, info_sent_metis, 'Metis', 'sentiment')
    note_difference(info_no_sent_metis, info_topic_metis, 'Metis', 'topic')
    note_difference(info_no_sent_metis, info_hybrid_metis, 'Metis', 'hybrid')

    
    # note_difference(info_no_sent_fluid, info_sent_fluid, 'Fluid')
    os.chdir(starting_path)
    log_write_start_end(False, 'Vax')
    