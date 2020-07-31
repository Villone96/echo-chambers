import networkx as nx
from networkx.algorithms.link_prediction import resource_allocation_index, preferential_attachment, jaccard_coefficient, adamic_adar_index
from link_prediction.home_made_link_prediction import get_edges_to_add_degree, get_edges_to_add_bet, add_top_deg_to_normal
from link_prediction.state_of_art_alg import get_edges_to_add
from link_prediction.link_pred_utilities import add_edges, add_sentiment_boost


def manage_sentiment(graph_name, selected_edges, shortest_path):
    tmp_graph = nx.read_gml(graph_name)
    edge_to_add = add_sentiment_boost(tmp_graph, selected_edges)
    selected_edges_sent = sorted(edge_to_add, key=lambda tup: tup[2], reverse=True)
    return add_edges(selected_edges_sent, tmp_graph, shortest_path*2)

def launch_all_link_prediction(graph_name, shortest_path, com_type, add_sent_boost):
    result = list()
    result_sentiment = list()

    ## ADAMIC 
    print('ADAMIC')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    selected_edges = get_edges_to_add(tmp_graph, adamic_adar_index, com_type, 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))

    if add_sent_boost == 1:
        print('SENTIMENT')
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path))

    ## RESOURCE ALLOCATION INDEX
    print('RESOURCE')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    selected_edges = get_edges_to_add(tmp_graph, resource_allocation_index, com_type, 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))

    if add_sent_boost == 1:
        print('SENTIMENT')
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path))

    ## TOP DEGREE
    print('TOP DEGREE')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    selected_edges = get_edges_to_add_degree(tmp_graph, com_type)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))

    if add_sent_boost == 1:
        print('SENTIMENT')
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path))

    ## TOP BET
    print('TOP BET')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    selected_edges = get_edges_to_add_bet(tmp_graph, com_type)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))

    if add_sent_boost == 1:
        print('SENTIMENT')
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path))


    ## NORMAL TO TOP DEGREE
    print('NORMAL TO TOP DEGREE')
    print('NO SENTIMENT')
    tmp_graph = nx.read_gml(graph_name)
    selected_edges = add_top_deg_to_normal(tmp_graph, com_type)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))

    if add_sent_boost == 1:
        print('SENTIMENT')
        result_sentiment.append(manage_sentiment(graph_name, selected_edges, shortest_path))
    print()



    return result, result_sentiment


'''



'''