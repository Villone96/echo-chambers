from tqdm import tqdm
from link_prediction.link_pred_utilities import add_sentiment_boost
from networkx.classes.function import non_edges

def get_edges_to_add(graph, metric, com_type, opt=0):
    to_add = list()
    total_weight = list()
    non_edge_in_graph = non_edges(graph)
    
    for edge in graph.edges(data=True):
        total_weight.append(edge[2]['weight'])
        
    max_edges_to_add = int(sum(total_weight)*0.3)
    
    for edge in tqdm(non_edge_in_graph):
        if graph.nodes[edge[0]][com_type] != graph.nodes[edge[1]][com_type]:
            result_of_metric = next(metric(graph, [edge]))
            if result_of_metric[2] > 0:
                to_add.append(result_of_metric)
                # print(len(to_add), end=" ")
            if len(to_add) > max_edges_to_add:
                break
    
    if opt == 1:
        edge_to_add = add_sentiment_boost(graph, to_add)
        sorted_to_add = sorted(edge_to_add, key=lambda tup: tup[2], reverse=True)
    else:
        sorted_to_add = sorted(to_add, key=lambda tup: tup[2], reverse=True)
    return sorted_to_add