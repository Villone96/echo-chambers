from preprocessing.ops_on_raw_data import check_directory_absence
import networkx as nx 
import pandas as pd
from tqdm import tqdm
import os
import ast

def graph_ops():
    garimella_graph()
    covid_graph()
    vax_graph()

def delete_not_useful_nodes_garimella(G):
    node_to_delete = []
    total_edge = 0
    for node in G.nodes():
        for edge in G.in_edges(node, data = True):
            total_edge += edge[2]['weight']
        for edge in G.out_edges(node, data = True):
            total_edge += edge[2]['weight']
        if total_edge < 3:
            node_to_delete.append(node)
        total_edge = 0
    
    G.remove_nodes_from(node_to_delete)
    largest_cc = max(nx.weakly_connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()

    return G

def build_garimella_graph(designed_datasets, path):
    for dataset in designed_datasets: 
        df = pd.read_csv(dataset)
        G = nx.DiGraph()
        [G.add_edge(row[0], row[1] , weight=row[2]) for _, row in df.iterrows()]
        graph_name = dataset.split('_')[2]
        G.name = 'Starter ' + graph_name
        print(nx.info(G))
        print()
        final_G = delete_not_useful_nodes_garimella(G)
        nx.write_gml(final_G, path + '/' + graph_name + '.gml')
        final_G.name = 'Final ' + graph_name
        print(nx.info(final_G))
        print('-----------------------------------------------')

def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data')
    if check_directory_absence('Graph', path):
        os.mkdir('Graph')
        os.chdir(os.path.join(path, 'retweet_networks'))

        designed_datasets = ['retweet_graph_ukraine_threshold_largest_CC.txt', 'retweet_graph_gunsense_threshold_largest_CC.txt',
                          'retweet_graph_baltimore_threshold_largest_CC.txt', 'retweet_graph_mothersday_threshold_largest_CC.txt',
                          'retweet_graph_jurassicworld_threshold_largest_CC.txt']

        build_garimella_graph(designed_datasets, os.path.join(path, 'Graph'))

    os.chdir(starting_path)

def build_covid_graph(path):
    df = pd.read_csv(path + '/final_data/' + 'Final_data.csv', lineterminator='\n')
    df.dropna(axis='index', how='all', subset=['text_con_hashtag'], inplace = True)
    # G = nx.DiGraph()
    G = nx.MultiDiGraph()
    for _, row in tqdm(df.iterrows(), desc = "Rows processed"):
        if row[4] == 'self':
            G = add_edge(G, row[5], 'covid', row[0], row[2], 0, row[3], row[3], True)
        else:
            mentions = row[4].split(',')
            for mention in mentions:
                mention = mention.strip()
                if mention != '' and mention != '@':
                    G = add_edge(G, row[5], 'covid', row[0], row[2], 0, row[3], mention, True)


    print('')
    G.name = 'Starter Covid Graph'
    print(nx.info(G))
    print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(G, 'count', True)))

    final_G = nodes_management(G, 'remove', True, 10)
    final_G.name = 'Final Covid Graph'

    print()
    print(nx.info(final_G))
    print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(final_G, 'count', True)))
    print('---------------------------------------')
    nx.write_gml(final_G, path + '/Graph/covid.gml')

def covid_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus')
    if check_directory_absence('Graph', path):
        os.mkdir('Graph')
        os.chdir(os.path.join(path, 'final_data'))
        build_covid_graph(path)

    os.chdir(starting_path)

def nodes_management(G, option, multi, threshold = 0):
    node_to_delete = []
    total_edge = 0
    
    if option == 'remove' or 'count':
        for node in G.nodes():
            for edge in G.in_edges(node, data = True):
                if not multi:
                    total_edge += edge[2]['nums']
                else:
                    total_edge += 1
            
            for edge in G.out_edges(node, data = True):
                if not multi:
                    total_edge += edge[2]['nums']
                else:
                    total_edge += 1

            if option == 'remove':
                if total_edge < threshold:
                    node_to_delete.append(node)
                total_edge = 0

        if option == 'remove':
            G.remove_nodes_from(node_to_delete)
            largest_cc = max(nx.weakly_connected_components(G), key=len)
            G = G.subgraph(largest_cc).copy()
            return G
        else:
            return total_edge/2
    else:
        print('BAD OPTION VALUE - TRY REMOVE OR COUNT')
        return -1

# Yes, I know, would be better RE :(
def clean(username):
    username = str(username)
    username = username.strip()
    username = username.split('\u2069')[0]
    username = username.split('.')[0]
    username = username.split("'")[0]
    username = username.split(")")[0]
    username = username.split("!")[0]
    username = username.split("?")[0]
    username = username.split('https')[0]
    username = username.split('http')[0]
    username = username.split('&#8217;s')[0]
    username = username.split('’')[0]
    username = username.split('より')[0]
    username = username.split('さんから')[0] 
    username = username.split('から')[0] 
    if username[-3:] == 'pic' and username.lower() != 'apic':
        username = username.split('pic')[0]
    username = username.lower()
    return username

def add_edge(G, tweet, hashtag, likes, retweets, replies, source, destination, multi):
    source = clean(source)
    destination = clean(destination)
    if multi:
        if hashtag == 'covid':
            G.add_edge(source, destination, tweet = tweet, likes = likes, retweets = retweets)
        else:
            G.add_edge(source, destination, tweet = tweet, hashtag = hashtag, likes = likes, 
                retweets = retweets, replies = replies)
        return G
    else:
        if G.has_edge(source, destination):
            G[source][destination]['tweets'].append(tweet)
            G[source][destination]['likes'].append(likes)
            G[source][destination]['retweets'].append(retweets)
            G[source][destination]['nums']+= 1
            if hashtag != 'covid':
                G[source][destination]['hashtags'].append(hashtag)
                G[source][destination]['replies'].append(replies)
        else:
            if hashtag == 'covid':
                G.add_edge(source, destination, tweets=[tweet], likes = [likes], retweets = [retweets], nums = 1)
            else:
                G.add_edge(source, destination, tweets=[tweet], hashtags=[hashtag], likes = [likes], 
                retweets = [retweets], replies = [replies], nums = 1)
        return G


def build_vaccination_graph(path):
    df = pd.read_csv(path + '/final_data/' + 'Final_data.csv', lineterminator='\n')
    # G = nx.DiGraph()
    G = nx.MultiDiGraph()
    num_nodes = 0
    num_edges = 0
    for _, row in tqdm(df.iterrows(), desc="Rows processed"):
        num_nodes += 1
        mentions = ast.literal_eval(row[3])
        if 'self' in mentions:
            G = add_edge(G, row[2], row[7], row[6], row[5], row[4], row[1], row[1], True)
            num_edges += 1
        else:
            for mention in mentions:
                G = add_edge(G, row[2], row[7], row[6], row[5], row[4], row[1], mention, True)
                num_edges += 1
                

    G.name = 'Starter Vaccination Graph'
    print(nx.info(G))
    print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(G, 'count', True)))

    final_G = nodes_management(G, 'remove', True, 3)
    final_G.name = 'Final Vaccination Graph'

    print()
    print(nx.info(final_G))
    print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(final_G, 'count', True)))
    print('---------------------------------------')
    nx.write_gml(final_G, path + '/Graph/vaccination.gml')


def vax_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax')
    if check_directory_absence('Graph', path):
        os.mkdir('Graph')
        os.chdir(os.path.join(path, 'final_data'))
        build_vaccination_graph(path)

    os.chdir(starting_path)
