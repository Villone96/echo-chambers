from tqdm import tqdm
from controversy_detection.change_side_controversy import change_side_controversy
from controversy_detection.GMCK import start_GMCK
from controversy_detection.random_walks import random_walks, random_walks_centrality
from matplotlib import pyplot as plt
import numpy as np

def add_sentiment_boost(graph, edge_to_add):
    
    total_edge = 0
    edge_with_sent = 0
    index = 0
    
    for edge in tqdm(edge_to_add):
        sentiment_similarity = int(60 - abs(graph.nodes[edge[0]]['sentiment'] - graph.nodes[edge[1]]['sentiment'])) + 1
        total_edge = 0
        edge_with_sent = 0
        
        for edge in graph.edges(data=True):
            if int(edge[2]['weightWithSentiment']) == sentiment_similarity:
                edge_with_sent += 1
            total_edge += 1
        edge_to_add[index] = (edge_to_add[index][0], edge_to_add[index][1], edge_to_add[index][2]*(edge_with_sent/total_edge))        
        index += 1
        
    return edge_to_add



def add_edges(all_edge_to_add, graph, avg_short_path, com_type='weightComm', opt=0):
    rw_value = list()
    rwc_value = list()
    change_side = list()
    gmck = list()
    
    
    total_weight = list()
    for edge in graph.edges(data=True):
        total_weight.append(edge[2]['weight'])
        
    weight = int(np.mean(total_weight))
    cont_to_add = int(sum(total_weight)*0.3)
    
    print_at = int(cont_to_add/30)
    
    cont = 0
    
    rw_value.append(random_walks(graph, 0.6, avg_short_path, opt, 1))
    rwc_value.append(random_walks_centrality(graph, opt, 1))
    change_side.append(change_side_controversy(graph, 0.6, avg_short_path, opt, 1))
    gmck.append(start_GMCK(graph, com_type, opt, 1))
    print()
    
    for edge in all_edge_to_add:
        graph.add_edge(edge[0], edge[1], weight=weight)
        cont_to_add -= weight
        cont += weight
        if cont >= print_at:
            rw_value.append(random_walks(graph, 0.6, avg_short_path, opt, 1))
            rwc_value.append(random_walks_centrality(graph, opt, 1))
            change_side.append(change_side_controversy(graph, 0.6, avg_short_path, opt, 1))
            gmck.append(start_GMCK(graph, com_type, opt, 1))
            print()
            cont = 0
        if cont_to_add < 0:
            rw_value.append(random_walks(graph, 0.6, avg_short_path, opt, 1))
            rwc_value.append(random_walks_centrality(graph, opt, 1))
            change_side.append(change_side_controversy(graph, 0.6, avg_short_path, opt, 1))
            gmck.append(start_GMCK(graph, com_type, opt, 1))
            print()
            break
            
    return [rw_value, rwc_value, change_side, gmck]


def plot_controversy_measure_line(values, title, no_contr_value):
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    marker = ["s", "8", "P", "*", "^", "."]
    colors = ['#0425e0', '#e0e004', '#ffd470', '#3c6b6b', '#720878']
    x_values = list()
    linestyle = [':', '-.', '--', '-', ':', '-.']
    labels = ['Adamic Adar Index', 'Resource Allocation Index', 'Top Degree Link Prediction', 'Top Betweness Link Prediction', 'Top to normal Degree Prediction']
    
    for i in range(0, 31):
        x_values.append(i/100)
        
    x_indexes = np.arange(len(x_values))
    
    for contr_value in values:
        index = values.index(contr_value)
        ax.plot(x_indexes, contr_value, color=colors[index], marker=marker[index], linestyle=linestyle[index], label=labels[index])
        
    ax.axhline(no_contr_value, color='#ff0000', label='Score su grafo senza controversy')
    ax.set_xlabel('% archi aggiunti')
    ax.set_ylabel('Score controversy')
    ax.set_title(title)
    ax.legend()
    
    plt.xticks(ticks=x_indexes, labels=x_values)

    plt.grid(True)

    plt.savefig(f'./{title}.png', dpi = 300, quality = 95, format = 'png', pad_inches = 1000)


    

