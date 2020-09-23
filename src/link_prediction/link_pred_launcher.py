import networkx as nx
from networkx.algorithms.link_prediction import resource_allocation_index, preferential_attachment, jaccard_coefficient, adamic_adar_index
from link_prediction.home_made_link_prediction import get_edges_to_add_degree, get_edges_to_add_bet, add_top_deg_to_normal
from link_prediction.state_of_art_alg import get_edges_to_add
from link_prediction.link_pred_utilities import add_edges, add_sentiment_boost
import os


def manage_sentiment(graph_name, selected_edges, shortest_path, save_name):
    tmp_graph = nx.read_gml(graph_name)
    edge_to_add = add_sentiment_boost(tmp_graph, selected_edges)
    selected_edges_sent = sorted(edge_to_add, key=lambda tup: tup[2], reverse=True)
    print(nx.info(tmp_graph))
    single_value = add_edges(selected_edges_sent, tmp_graph, shortest_path*2, 'sentimentComm', 1)
    nx.write_gml(tmp_graph, f'./{save_name}.gml')
    print(nx.info(tmp_graph))
    return single_value

def launch_all_link_prediction(graph_name, shortest_path, com_type, add_sent_boost):
    result = list()
    result_sentiment = list()

    if com_type == 'sentimentComm':
        opt = 1
    else:
        opt = 0

    ## ADAMIC 
    print('ADAMIC')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    print(nx.info(tmp_graph))
    selected_edges = get_edges_to_add(tmp_graph, adamic_adar_index, com_type, 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2, com_type, opt))
    print(nx.info(tmp_graph))
    name = graph_name.split('.')[0]+'_ADAMIC'
    nx.write_gml(tmp_graph, f'./{name}.gml')

    if add_sent_boost == 1:
        print('SENTIMENT')
        name = graph_name.split('.')[0]+'_ADAMIC_SENT'
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path, name))
    print()

    ## JACCARD COEFFICIENT INDEX
    print('JACCARD_COEFFICIENT')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    print(nx.info(tmp_graph))
    selected_edges = get_edges_to_add(tmp_graph, jaccard_coefficient, com_type, 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2, com_type, opt))
    print(nx.info(tmp_graph))
    name = graph_name.split('.')[0]+'_JACCARD_COEFFICIENT'
    nx.write_gml(tmp_graph, f'./{name}.gml')
    

    if add_sent_boost == 1:
        print('SENTIMENT')
        name = graph_name.split('.')[0]+'_JACCARD_COEFFICIENT_SENT'
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path, name))
    print()

    ## TOP DEGREE
    print('TOP DEGREE')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    print(nx.info(tmp_graph))
    selected_edges = get_edges_to_add_degree(tmp_graph, com_type)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2, com_type, opt))
    print(nx.info(tmp_graph))
    name = graph_name.split('.')[0]+'_TOP_DEGREE'
    nx.write_gml(tmp_graph, f'./{name}.gml')

    if add_sent_boost == 1:
        print('SENTIMENT')
        name = graph_name.split('.')[0]+'_TOP_DEGREE_SENT'
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path, name))
    print()

    ## TOP BET
    print('TOP BET')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    print(nx.info(tmp_graph))
    selected_edges = get_edges_to_add_bet(tmp_graph, com_type)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2, com_type, opt))
    print(nx.info(tmp_graph))
    name = graph_name.split('.')[0]+'_TOP_BET'
    nx.write_gml(tmp_graph, f'./{name}.gml')

    if add_sent_boost == 1:
        print('SENTIMENT')
        name = graph_name.split('.')[0]+'_TOP_BET_SENT'
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path, name))
    print()


    ## NORMAL TO TOP DEGREE
    print('NORMAL TO TOP DEGREE')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    print(nx.info(tmp_graph))
    selected_edges = add_top_deg_to_normal(tmp_graph, com_type)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2, com_type, opt))
    print(nx.info(tmp_graph))
    name = graph_name.split('.')[0]+'_NORMAL_TOP_DEGREE'
    nx.write_gml(tmp_graph, f'./{name}.gml')

    if add_sent_boost == 1:
        print('SENTIMENT')
        name = graph_name.split('.')[0]+'_NORMAL_TOP_DEGREE_SENT'
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path, name))
    print()

    return result, result_sentiment