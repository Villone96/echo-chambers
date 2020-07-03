
from tqdm import tqdm
import logging

def satisfy_second_condition(node1, graph, dict_left, dict_right, cut):
    # A node v in G_i has at least one edge connecting to a member of G_i which is not connected to G_j.
    neighbors = graph.neighbors(node1)
    for n in neighbors:
        if node1 in dict_left and n in dict_right:  # only consider neighbors belonging to G_i
            continue
        if node1 in dict_right and n in dict_left:  # only consider neighbors belonging to G_i
            continue
        if n not in cut:
            return True
    return False


def lists_to_dict(keys: list, values: list):
    if len(keys) != len(values):
        raise Exception("Two lists are not of the same length")
    keys_and_values = dict(zip(keys, values))
    return keys_and_values


def start_GMCK(graph, com_type):
    logging.basicConfig(filename='controversy_detection.log', level=logging.INFO, format='%(message)s')
    left = list()
    right = list()

    for node in graph.nodes(data=True):
        if node[1][com_type] == 0:
            left.append(node[0])
        else:
            right.append(node[0])
            
    dict_left = lists_to_dict(left, [1] * len(left))
    dict_right = lists_to_dict(right, [1] * len(right))
    cut_nodes1 = {}
    cut_nodes = {}
    for i in tqdm(range(len(left))):
        name1 = left[i]
        for j in range(len(right)):
            name2 = right[j]
            if graph.has_edge(name1, name2):
                cut_nodes1[name1] = 1
                cut_nodes1[name2] = 1
                
    dict_across = {}  # num. edges across the cut
    dict_internal = {}  # num. edges internal to the cut

    for keys in cut_nodes1.keys():

        if satisfy_second_condition(keys, graph, dict_left, dict_right, cut_nodes1):
            cut_nodes[keys] = 1

    for edge in graph.edges():
        node1 = edge[0]
        node2 = edge[1]
        
        if node1 not in cut_nodes and (node2 not in cut_nodes):  # only consider edges involved in the cut
            continue
        if node1 in cut_nodes and node2 in cut_nodes:
            # if both nodes are on the cut and both are on the same side, ignore
            if node1 in dict_left and node2 in dict_left:
                continue
            if node1 in dict_right and node2 in dict_right:
                continue
        if node1 in cut_nodes:
            if node1 in dict_left:
                if node2 in dict_left and node2 not in cut_nodes1:
                    if node1 in dict_internal:
                        dict_internal[node1] += 1
                    else:
                        dict_internal[node1] = 1
                elif node2 in dict_right and node2 in cut_nodes:
                    if node1 in dict_across:
                        dict_across[node1] += 1
                    else:
                        dict_across[node1] = 1
            elif node1 in dict_right:
                if node2 in dict_left and node2 in cut_nodes:
                    if node1 in dict_across:
                        dict_across[node1] += 1
                    else:
                        dict_across[node1] = 1
                elif node2 in dict_right and node2 not in cut_nodes1:
                    if node1 in dict_internal:
                        dict_internal[node1] += 1
                    else:
                        dict_internal[node1] = 1
        if node2 in cut_nodes:
            if node2 in dict_left:
                if node1 in dict_left and node1 not in cut_nodes1:
                    if node2 in dict_internal:
                        dict_internal[node2] += 1
                    else:
                        dict_internal[node2] = 1
                elif node1 in dict_right and node1 in cut_nodes:
                    if node2 in dict_across:
                        dict_across[node2] += 1
                    else:
                        dict_across[node2] = 1
            elif node2 in dict_right:
                if node1 in dict_left and node1 in cut_nodes:
                    if node2 in dict_across:
                        dict_across[node2] += 1
                    else:
                        dict_across[node2] = 1
                elif node1 in dict_right and node1 not in cut_nodes1:
                    if node2 in dict_internal:
                        dict_internal[node2] += 1
                    else:
                        dict_internal[node2] = 1

    polarization_score = 0.0
    for keys in cut_nodes.keys():
        if keys not in dict_internal or (keys not in dict_across):  # for singleton nodes from the cut
            continue
        if dict_across[keys] == 0 and dict_internal[keys] == 0:  # there's some problem
            print("wtf")
        polarization_score += (dict_internal[keys] * 1.0 / (dict_internal[keys] + dict_across[keys]) - 0.5)

    polarization_score = round(polarization_score / len(cut_nodes.keys()), 4)
    print(f'GMCK score: {round(polarization_score, 4)}')
    logging.info(f'GMCK score: {round(polarization_score, 4)}')