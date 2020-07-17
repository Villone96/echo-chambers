import random
from controversy_detection.controversy_utilities import create_multi_graph
import numpy as np
import logging

def change_side_controversy(start_graph, sample_size, num_steps, opt=0, plot=0):

    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    
    for_community_0 = 0
    for_community_1 = 0
    if opt == 0:
        com_type = 'weightComm'
    elif opt == 1:
        com_type = 'sentimentComm'
    elif opt == 2:
        com_type = 'topicComm'
    graph = create_multi_graph(start_graph, opt)
    result = list()
    
    for node in graph.nodes(data=True):
        if node[1]['com'] == 0:
            for_community_0 += 1
        else:
            for_community_1 += 1
            
    for_community_0 = int(for_community_0*sample_size)
    for_community_1 = int(for_community_1*sample_size)
    
    sample_com_0 = for_community_0
    sample_com_1 = for_community_1
    
    already_taken = list()
    
    while True:
        node_id = random.randint(0, len(graph)-1)
        for node in graph.nodes(data=True):
            if node[1]['id'] == node_id:
                break
        if len(list(graph.edges(node[0]))) > 0 and node_id not in already_taken:
            already_taken.append(node_id)
            com = node[1]['com']
            if not((for_community_0 == 0 and com == 0) or (for_community_1 == 0 and com == 1)):
                
                result.append(start_random_walks_side(node, graph, num_steps))
                if com == 0:
                    for_community_0 -= 1
                else:
                    for_community_1 -= 1
                
                # print(for_community_0 + for_community_1)
                    
                if int(for_community_0 + for_community_1) <= 0:
                    break
                elif (for_community_0 + for_community_1) == int((sample_com_0 + sample_com_1)*0.75):
                    print('25% of node processed')
                elif (for_community_0 + for_community_1) == int((sample_com_0 + sample_com_1)*0.5):
                    print('50% of node processed')
                elif (for_community_0 + for_community_1) == int((sample_com_0 + sample_com_1)*0.25):
                    print('75% of node processed')
                    
    score = np.mean(result)
    print(f'Change side controversy for {com_type}: {np.mean(score)}')
    if plot == 1:
        return np.mean(round(score, 4))
    else:
        logging.info(f'Change side controversy score for {com_type}: {round(score, 4)}')
    
def start_random_walks_side(node, graph, steps):
    max_restart = 20
    result = 0
    cont = 0
    start_node_com = node[1]['com']
    steps_done = 0
    
    change_times = 0
    
    #print(f'SELECTED NODE: {node[0]}')
    #print(f'STARTER NODE COMMUNITY: {start_node_com}')
    
    current_node = node[0]
    
    while steps_done <= steps:
        list_edges = list(graph.edges(current_node))
        if len(list_edges) != 0:
            next_node = list_edges[random.randint(0,len(list_edges)-1)][1]
            if graph.nodes[next_node]["com"] != start_node_com:
                change_times += 1
            steps_done += 1
    result = 1 - (change_times/steps)
    #print(f'RISULTATO: {result}')
    #print(f'Restart: {max_restart}')
    return result