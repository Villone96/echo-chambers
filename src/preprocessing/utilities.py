import pandas as pd
import networkx as nx

def get_only_date(date):
    date = str(date).split()[0]
    return date

def get_metadata():
    user_metadata = pd.read_csv('./user_metadata/user_metadata.csv', engine='python')
    user_metadata.fillna(value = pd.np.nan, inplace = True)

    user_metadata['description'] = user_metadata['description'].fillna('NoDescription')
    user_metadata['location'] = user_metadata['location'].fillna('NoLocation')
    user_metadata['favourites_count'] = user_metadata['favourites_count'].fillna('-1')
    user_metadata['followers_count'] = user_metadata['followers_count'].fillna('-1')
    user_metadata['friends_count'] = user_metadata['friends_count'].fillna('-1')
    user_metadata['listed_count'] = user_metadata['listed_count'].fillna('-1')
    user_metadata['statuses_count'] = user_metadata['statuses_count'].fillna('-1')
    user_metadata['verified'] = user_metadata['verified'].fillna('-1')

    user_metadata['screen_name'] = user_metadata['screen_name'].str.lower()
    user_metadata['created_at'] = user_metadata['created_at'].apply(get_only_date)

    user_metadata = user_metadata.drop_duplicates(subset='screen_name', keep='last')
    user_metadata = user_metadata.rename(columns={'created_at': 'created', 'default_profile_image': 'DefaultImage', 
                                                  'favourites_count': 'numLikes', 'followers_count': 'numFollowers', 'friends_count': 'numFollowing',
                                                  'listed_count': 'numGroups', 'statuses_count': 'numStatuses', 'default_profile': 'defaultProfile'})
    user_metadata.set_index('screen_name', inplace = True)
    return user_metadata

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
    username = username.split(';')[0] 
    username = username.split('*')[0] 
    if username[-3:] == 'pic' and username.lower() != 'apic':
        username = username.split('pic')[0]
    username = username.lower()
    return username

def nodes_management(G, option, multi,threshold = 0):
    node_to_delete = []
    total_edge = 0
    
    if option == 'remove' or 'count':
        for node in G.nodes():
            if type(G).__name__ == 'DiGraph':
                total_edge += G.in_degree([node], weight='weight')[node]
                total_edge += G.out_degree([node], weight='weight')[node]
            else:
                if multi:
                    total_edge += G.degree(node)
                else:
                    total_edge += G.degree([node], weight='weight')[node]

            if option == 'remove':
                if total_edge < threshold:
                    node_to_delete.append(node)
                total_edge = 0

        if option == 'remove':
            G.remove_nodes_from(node_to_delete)
            if type(G).__name__ == 'DiGraph':
                largest_cc = max(nx.weakly_connected_components(G), key=len)
            else:
                largest_cc = max(nx.connected_components(G), key=len)

            G = G.subgraph(largest_cc).copy()
            return G
        else:
            return total_edge/2
    else:
        print('BAD OPTION VALUE - TRY REMOVE OR COUNT')
        return -1

def add_edge(G, tweet, hashtag, likes, retweets, replies, source, destination):
    source = clean(source)
    destination = clean(destination)

    if type(G).__name__ == 'DiGraph':
        if G.has_edge(source, destination):
            G[source][destination]['tweets'].append(tweet)
            G[source][destination]['likes'].append(likes)
            G[source][destination]['retweets'].append(retweets)
            G[source][destination]['weight']+= 1.0
            if hashtag != 'covid':
                G[source][destination]['hashtags'].append(hashtag)
                G[source][destination]['replies'].append(replies)
        else:
            if hashtag == 'covid':
                G.add_edge(source, destination, tweets=[tweet], likes = [likes], retweets = [retweets], weight = 1.0)
            else:
                G.add_edge(source, destination, tweets=[tweet], hashtags=[hashtag], likes = [likes], 
                retweets = [retweets], replies = [replies], weight = 1.0)
    else:
        if type(G).__name__ == 'MultiGraph':
            G.add_edge(source, destination)
        elif type(G).__name__ == 'Graph':
            if G.has_edge(source, destination):
                G[source][destination]['weight'] += 1.0
            else:
                G.add_edge(source, destination, weight = 1.0)
    return G

def manage_and_save(graphs, path):

    for graph in graphs: 

        name = 'Final_'+type(graph).__name__
        if 'Multi' in graph.name:
            multi = True
        else:
            multi = False
        
        if 'vax' in graph.name:
            threshold = 3
            name = name + '_Vax'
        else:
            threshold = 10
            name = name + '_Covid'

        name = name + '.gml'

        print(nx.info(graph))
        print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(graph, 'count', multi)))
        print()

        graph = nodes_management(graph, 'remove', multi, threshold)
        graph.name = graph.name.replace('Starter', 'Final')
        print(nx.info(graph))
        print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(graph, 'count', multi)))
        print()

        nx.write_gml(graph, path + '/Graph/' + name)


def delete_not_useful_nodes_garimella(G):
    node_to_delete = []
    total_edge = 0
    for node in G.nodes():
        total_edge += G.degree([node], weight='weight')[node]
        if total_edge < 3:
            node_to_delete.append(node)
        total_edge = 0
    
    G.remove_nodes_from(node_to_delete)
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()

    return G

def create_multi_graph(G):
    G_multi = nx.MultiGraph()
    G_multi.name = 'Final multi ' + G.name.split('graph')[-1]

    for edge in G.edges(data = True):
        weight = edge[2]['weight']
        for _ in range(int(weight)):
            G_multi.add_edge(edge[0], edge[1])
    
    return G_multi