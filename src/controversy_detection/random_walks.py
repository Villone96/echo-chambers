import random
from networkx.algorithms.centrality import degree_centrality
from controversy_detection.controversy_utilities import create_multi_graph
import logging

def random_walks(start_graph, sample_size, num_steps, opt=0, plot=0):
    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    for_community_0 = 0
    for_community_1 = 0
    
    start_0_end_0 = 0
    start_0_end_1 = 0
    
    start_1_end_1 = 0
    start_1_end_0 = 0
    if opt == 0:
        com_type = 'weightComm'
    elif opt == 1:
        com_type = 'sentimentComm'
    elif opt == 2:
        com_type = 'topicComm'
    graph = create_multi_graph(start_graph, opt)

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
                
                result = start_random_walks(node, graph, num_steps)

                if result != 4:
                    if com == 0:
                        for_community_0 -= 1
                    else:
                        for_community_1 -= 1

                    if result == 0:
                        start_0_end_0 += 1
                    elif result == 1:
                        start_1_end_0 += 1
                    elif result == 2:
                        start_0_end_1 += 1
                    else:
                        start_1_end_1 += 1
                else:
                    print('-4')
                    
                if int(for_community_0 + for_community_1) <= 0:
                    break
                elif (for_community_0 + for_community_1) == int((sample_com_0 + sample_com_1)*0.75):
                    pass
                    #print('25% of node processed')
                elif (for_community_0 + for_community_1) == int((sample_com_0 + sample_com_1)*0.5):
                    pass
                    #print('50% of node processed')
                elif (for_community_0 + for_community_1) == int((sample_com_0 + sample_com_1)*0.25):
                    pass
                    #print('75% of node processed')
                    
    #print(f'start_0_end_0: {start_0_end_0}')
    #print(f'start_1_end_0: {start_1_end_0}')
    #print(f'start_0_end_1: {start_0_end_1}')
    #print(f'start_1_end_1: {start_1_end_1}')
    #print()
    
    start_0_end_0 = start_0_end_0/(sample_com_0)    
    start_1_end_0 = start_1_end_0/(sample_com_1)    
    start_0_end_1 = start_0_end_1/(sample_com_0)    
    start_1_end_1 = start_1_end_1/(sample_com_1)  
    #print()
                    
    #print(f'start_0_end_0: {start_0_end_0}')
    #print(f'start_1_end_0: {start_1_end_0}')
    #print(f'start_0_end_1: {start_0_end_1}')
    #print(f'start_1_end_1: {start_1_end_1}') 
    score = start_0_end_0*start_1_end_1-start_1_end_0*start_0_end_1
    # print(f'RandomWalk random score for {com_type}: {round(score, 4)}')
    if plot == 1:
        return round(score, 4)
    else:
        logging.info(f'RandomWalk random score for {com_type}: {round(score, 4)}')

def start_random_walks(node, graph, steps):
    max_restart = 20
    result = 0
    cont = 0
    start_node_com = node[1]['com']
    steps_done = 0
    
    #print(f'SELECTED NODE: {node[0]}')
    #print(f'STARTER NODE COMMUNITY: {start_node_com}')
    
    current_node = node[0]
    
    while steps_done <= steps:
        list_edges = list(graph.edges(current_node))
        if len(list_edges) != 0:
            next_node = list_edges[random.randint(0,len(list_edges)-1)][1]
            #print(f'Next node: {next_node}')
            #print(f'Next node com: {graph.nodes[next_node]["com"]}')
            steps_done += 1
        else:
            max_restart -= 1
            if max_restart == -1:
                result = 4
                break
            current_node = node[0]
            steps_done = 0
            
    if max_restart != -1:
        if graph.nodes[next_node]["com"] == 0:
            if start_node_com == 0:
                result = 0
            else:
                result = 1
        elif graph.nodes[next_node]["com"] == 1:
            if start_node_com == 0:
                result = 2
            else:
                result = 3
    
    #print(f'RISULTATO: {result}')
    #print(f'Restart: {max_restart}')
    return result


def top_out_degree(graph, perc, com, opt=0):
    cont_com = 0
    
    for node in graph.nodes(data=True):
        if node[1]['com'] == com:
            cont_com += 1
    
    num_nodes = int(cont_com * (perc/100))
    
    top_out_degree = degree_centrality(graph)
    top_out_degree_sorted = {k: v for k, v in sorted(top_out_degree.items(), key=lambda item: item[1], reverse=True)}
    
    top_user = list()
    for node in top_out_degree_sorted:
        if graph.nodes[node]['com'] == com:
            if opt == 1:
                top_user.append((node, top_out_degree_sorted[node]))
            else:
                top_user.append(node)
            num_nodes -= 1
        if num_nodes == 0:
            break 
            
    return top_user
    
    
def random_walks_centrality(start_graph, opt=0, plot=0):
    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    if opt == 0:
        com_type = 'weightComm'
    elif opt == 1:
        com_type = 'sentimentComm'
    elif opt == 2:
        com_type = 'topicComm'
    graph = create_multi_graph(start_graph, opt)
    top_com_0 = top_out_degree(graph, 25, 0)
    top_com_1 = top_out_degree(graph, 25, 1)
    
    start_0_end_0 = 0
    start_0_end_1 = 0
    
    start_1_end_1 = 0
    start_1_end_0 = 0
    
    for top_node in top_com_0:
        for node in graph.nodes(data=True):
            if node[0] == top_node:
                break 
                
        result = start_random_walks_centrality(node, graph, top_com_0, top_com_1)
        
        if result == 0:
            start_0_end_0 += 1
        elif result == 1:
            start_1_end_0 += 1
        elif result == 2:
            start_0_end_1 += 1
        else:
            start_1_end_1 += 1
    
            
    for top_node in top_com_1:
        for node in graph.nodes(data=True):
            if node[0] == top_node:
                break 
        result = start_random_walks_centrality(node, graph, top_com_0, top_com_1)
        
        if result == 0:
            start_0_end_0 += 1
        elif result == 1:
            start_1_end_0 += 1
        elif result == 2:
            start_0_end_1 += 1
        else:
            start_1_end_1 += 1
          
    #print(f'start_0_end_0: {start_0_end_0}')
    #print(f'start_1_end_0: {start_1_end_0}')
    #print(f'start_0_end_1: {start_0_end_1}')
    #print(f'start_1_end_1: {start_1_end_1}')
    #print()
    
    start_0_end_0 = start_0_end_0/(len(top_com_0))    
    start_1_end_0 = start_1_end_0/(len(top_com_1))   
    start_0_end_1 = start_0_end_1/(len(top_com_0))   
    start_1_end_1 = start_1_end_1/(len(top_com_1)) 
    #print()
                    
    #print(f'start_0_end_0: {start_0_end_0}')
    #print(f'start_1_end_0: {start_1_end_0}')
    #print(f'start_0_end_1: {start_0_end_1}')
    #print(f'start_1_end_1: {start_1_end_1}')    
    score = start_0_end_0*start_1_end_1-start_1_end_0*start_0_end_1
    #print(f'RandomWalk top degree score for {com_type}: {round(score, 4)}')
    #print()
    if plot == 1:
        return round(score, 4)
    else:
        logging.info(f'RandomWalk top degree score for {com_type}: {round(score, 4)}')

# result legend
# 0: start in 0 and end in 0
# 1 : start in 1 and end in 0
# 2: start in 0 and end in 1
# 3: start in 1 and end in 1
# 4: to much restart

def start_random_walks_centrality(node, graph, top_com_0, top_com_1):
    result = 0
    start_node_com = node[1]['com']
    
    # print(f'SELECTED NODE: {node[0]}')
    # print(f'STARTER NODE COMMUNITY: {start_node_com}')
    
    current_node = node[0]
    
    while True:
        list_edges = list(graph.edges(current_node))
        next_node = list_edges[random.randint(0,len(list_edges)-1)][1]
        if graph.nodes[next_node]["com"] == 0:
            if start_node_com == 0:
                result = 0
            else:
                result = 1
            break
        elif graph.nodes[next_node]["com"] == 1:
            if start_node_com == 0:
                result = 2
            else:
                result = 3
            break
    return result