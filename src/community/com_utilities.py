import networkx as nx
from networkx.algorithms.community.quality import coverage 
from tqdm import tqdm
import networkx.algorithms.community as nx_comm
import nxmetis
import time
from math import ceil
from random import random, randint
from collections import Counter

from community.log_writer import log_write_com_result, log_write_graph_info, print_difference


def create_multi_graph(G):
    G_multi = nx.MultiGraph()
    for edge in G.edges(data = True):
        weight = ceil(edge[2]['weightWithSentiment'])
        for _ in range(weight):
            G_multi.add_edge(edge[0], edge[1])

    return G_multi


def modularity(partition, graph, weight='weight'):
    if graph.is_directed():
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = graph.size(weight=weight)
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph:
        com = partition[node]
        deg[com] = deg.get(com, 0.) + graph.degree(node, weight=weight)
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor == node:
                    inc[com] = inc.get(com, 0.) + float(edge_weight)
                else:
                    inc[com] = inc.get(com, 0.) + float(edge_weight) / 2.

    res = 0.
    for com in set(partition.values()):
        res += (inc.get(com, 0.) / links) - \
               (deg.get(com, 0.) / (2. * links)) ** 2
    return res

def get_community_dict_and_set(list_com):
    '''
    From communities partitions returns a list of set
    and dictionary of these
    '''
    com = 0
    commun_dict = dict()
    commun_list = list()
    single_com = set()

    for communities in list_com:
        for member in communities:
            commun_dict[member] = com
            single_com.add(member)
        com += 1
        commun_list.append(single_com)
        single_com = set()
    return commun_dict, commun_list


def get_communities(G, alg, sent, k = 0, seed = 0):
    raw_partition = list()
    list_com = list()
    set_com = set()
    info = list()
    start = 0
    end = 0

    if sent:
        weight = 'weightWithSentiment'
    else:
        weight = 'weight'

    if alg == 'Metis':
        for edge in G.edges(data=True):
            G[edge[0]][edge[1]][weight] = int(G[edge[0]][edge[1]][weight])
        start = time.time()
        raw_partition = nxmetis.partition(G, 2, edge_weight=weight, node_weight=None, node_size=None)
        end = time.time()
        list_com, set_com = get_community_dict_and_set(raw_partition[1])

        print(f'Lenght community 0: {len(raw_partition[1][0])}')
        print(f'Lenght community 1: {len(raw_partition[1][1])}')

        info = [len(raw_partition[1][0]), len(raw_partition[1][1])]
    elif alg == 'Fluid':
        communities: Dict[int, set] = dict()
        start = time.time()
        partitions = nx_comm.asyn_fluidc(G, k=k, seed=seed)
        end = time.time()
        for p in range(k):
            communities[p] = next(partitions)
        raw_partition.append(communities[0])
        raw_partition.append(communities[1])
        print(f'Lenght community 0: {len(raw_partition[0])}')
        print(f'Lenght community 1: {len(raw_partition[1])}')

        list_com, set_com = get_community_dict_and_set(raw_partition)

        info = [len(raw_partition[0]), len(raw_partition[1])]
    else:
        print('Wrong algorithm name')
        set_com = -1
        list_com = -1
        info = -1

    return list_com, set_com, info, end-start

def label_node_communities(G, communities):
    for member in communities:
        G.nodes[member]['community'] = communities[member]
    return G   

def extract_community(G, id_com):
    community_node = list()
    
    for node in G.nodes():
        if  G.nodes[node]['community'] != id_com:
            community_node.append(node)
    subgraph = G.subgraph(community_node)
    return subgraph

def community_detection(name, opt, sent=False):
    #### READING GRAPH
    ## OPT == 0 --> Garimella ELSE VAX/COVID
    if opt == 0:
        graph = nx.read_gml(f'{name}.gml')
        multi = nx.read_gml(f'Multi_{name}.gml')
    else:
        graph = nx.read_gml(f'Final_Graph_{name}.gml')
        multi = nx.read_gml(f'Final_MultiGraph_{name}.gml')
    if not sent:
        log_write_graph_info(name, nx.info(graph), nx.info(multi))
    #### METIS
    list_com_metis, set_com_metis, info, exe_time = get_communities(graph, 'Metis', sent)
    mod_m = modularity(list_com_metis, graph, weight='weight')
    cov_m = coverage(multi, set_com_metis)
    log_write_com_result('Metis', info, mod_m, cov_m, exe_time, opt, sent)
    
    #### FLUID
    seed = 1
    if opt == 1:
        seed = 18
    if sent:
        multi_fluid = create_multi_graph(graph)
        if name == 'Covid':
            seed = 76
        else:
            seed = 38
    else:
        multi_fluid = multi
    # print('BEFORE')
    # print(nx.info(multi_fluid))
    # print()
    list_com_fluid, set_com_fluid, info, exe_time = get_communities(multi_fluid, 'Fluid', sent, 2, seed)

    # print()
    # print(Counter(list_com_fluid.values()))
    # print()
    mod_f = modularity(list_com_fluid, graph, weight='weight')
    cov_f = coverage(multi, set_com_fluid)
    log_write_com_result('Fluid', info, mod_f, cov_f, exe_time, opt, sent)
    return [list_com_metis, mod_m, cov_m], [list_com_fluid, mod_f, cov_f]


def note_difference(info_no_sent, info_sent, alg):

    same = 0
    notsame = 0
    no_sent = info_no_sent[0]
    sent = info_sent[0]
    for user in no_sent:
        if no_sent[user] == sent[user]:
            same += 1
        else:
            notsame += 1

    mod_difference = info_sent[1] - info_no_sent[1]
    cov_difference = info_sent[2] - info_no_sent[2]

    print_difference(alg, same, notsame, mod_difference, cov_difference)
    
