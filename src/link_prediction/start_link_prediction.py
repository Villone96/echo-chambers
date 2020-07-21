import os
import random
import networkx as nx

from link_prediction.state_of_art_alg import get_edges_to_add
from networkx.algorithms.link_prediction import resource_allocation_index, preferential_attachment, jaccard_coefficient, adamic_adar_index
from link_prediction.link_pred_utilities import add_edges, plot_controversy_measure_line, plot_controversy_sentiment_match, launch_all_link_prediction
from link_prediction.home_made_link_prediction import get_edges_to_add_degree, get_edges_to_add_bet, add_top_deg_to_normal

from networkx.algorithms.shortest_paths.generic import average_shortest_path_length

def start_link_opt():
    #garimella()
    covid()
    vaccination()


def garimella():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data/Graph')
    os.chdir(path)
    list_of_graph = os.listdir(path)
    contr_detect_method = ['RandomWalks', 'RandomWalks top degree', 'Change Side', 'GMCK']
    no_contr_values = [0.4933, 0.6869,  0.7436, 0.0213]

    for graph in list_of_graph:
        name = graph
        if 'Multi' in name or 'log' in name or 'kissing' in name or 'png' in name:
            continue
        else:
            print(name)
            name = name.split('.')[0]
            graph = nx.read_gml(f'{name}.gml')
            shortest_path = average_shortest_path_length(graph)
            result = launch_all_link_prediction(f'{name}.gml', shortest_path, 'weightComm', 0)

            for i in range(4):
                single_target = list()
                for j in range(len(result)):
                    single_target.append(result[j][i])

                plot_controversy_measure_line(single_target, f'Riduzione controversy per {name} data {contr_detect_method[i]} controversy', no_contr_values[i])

    os.chdir(starting_path)

def covid():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus/Graph')
    os.chdir(path)
    contr_detect_method = ['RandomWalks', 'RandomWalks top degree', 'Change Side', 'GMCK']
    labels = ['Adamic Adar Index', 'Resource Allocation Index', 'Top Degree Link Prediction', 'Top Betweness Link Prediction', 'Top to normal Degree Prediction']
    no_contr_values = [0.4933, 0.6869,  0.7436, 0.0213]
    result = list()
    result_sentiment = list()

    # shortest_path = average_shortest_path_length(tmp_graph)
    shortest_path = 25.596369322723653

    print('adamic_adar_index')
    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges_sent = get_edges_to_add(tmp_graph, adamic_adar_index, 'sentimentComm', 1)
    result_sentiment.append(add_edges(selected_edges_sent, tmp_graph, shortest_path*2))

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges = get_edges_to_add(tmp_graph, adamic_adar_index, 'sentimentComm', 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
    print()


    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges_sent = get_edges_to_add(tmp_graph, resource_allocation_index, 'sentimentComm', 1)
    result_sentiment.append(add_edges(selected_edges_sent, tmp_graph, shortest_path*2))

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges = get_edges_to_add(tmp_graph, resource_allocation_index, 'sentimentComm', 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
    print()


    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges_sent = get_edges_to_add_degree(tmp_graph, 'sentimentComm', 1)
    result_sentiment.append(add_edges(selected_edges_sent, tmp_graph, shortest_path*2))

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges = get_edges_to_add_degree(tmp_graph, 'sentimentComm')
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
    print()

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges_sent = get_edges_to_add_bet(tmp_graph, 'sentimentComm', 1)
    result_sentiment.append(add_edges(selected_edges_sent, tmp_graph, shortest_path*2))

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges = get_edges_to_add_bet(tmp_graph, 'sentimentComm')
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
    print()

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges_sent = add_top_deg_to_normal(tmp_graph, 'sentimentComm', 1)
    result_sentiment.append(add_edges(selected_edges_sent, tmp_graph, shortest_path*2))

    tmp_graph = nx.read_gml('Final_Graph_Covid.gml')
    selected_edges = add_top_deg_to_normal(tmp_graph, 'sentimentComm', 0)
    result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
    print()

    for i in range(4):
        single_target = list()
        for j in range(len(result)):
            single_target.append(result[j][i])

        plot_controversy_measure_line(single_target, f'Riduzione controversy per Covid-19 data {contr_detect_method[i]} controversy', no_contr_values[i])

    for i in range(len(result)):
        for j in range(len(result[i])):
            plot_controversy_sentiment_match(result[i][j], result_sentiment[i][j], f'Differenza riduzione controversy per Covid-19 tenendo conto del sentiment data {contr_detect_method[j]} controversy',  no_contr_values[i], labels[i])

    os.chdir(starting_path)


def vaccination():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax/Graph')
    os.chdir(path)
    contr_detect_method = ['RandomWalks', 'RandomWalks top degree', 'Change Side', 'GMCK']
    no_contr_values = [0.4933, 0.6869,  0.7436, 0.0213]

    os.chdir(starting_path)






'''
            print(name)

            print('adamic_adar_index')
            tmp_graph = nx.read_gml(f'{name}.gml')
            selected_edges = get_edges_to_add(tmp_graph, adamic_adar_index, 'weightComm', 0)
            result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
            print()

            print('resource_allocation_index')
            tmp_graph = nx.read_gml(f'{name}.gml')
            selected_edges = get_edges_to_add(tmp_graph, resource_allocation_index, 'weightComm', 0)
            result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
            print()

            print('top degree add')
            tmp_graph = nx.read_gml(f'{name}.gml')
            selected_edges = get_edges_to_add_degree(tmp_graph, 'weightComm')
            result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
            print()

            print('top bet add')
            tmp_graph = nx.read_gml(f'{name}.gml')
            selected_edges = get_edges_to_add_bet(tmp_graph, 'weightComm')
            result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
            print()

            tmp_graph = nx.read_gml(f'{name}.gml')
            selected_edges = add_top_deg_to_normal(tmp_graph, 'weightComm', 0)
            result.append(add_edges(selected_edges, tmp_graph, shortest_path*2))
            print()


'''