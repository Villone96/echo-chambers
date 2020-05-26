import pandas as pd
import networkx as nx
import re 

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

def nodes_management(G, option, threshold = 0):
    edge_to_delete = []
    total_edge = 0
    real_edge = 0
  
    if option == 'remove' or 'count':
        edge_to_delete = list()
        for edge in G.edges(data=True):
            if type(G).__name__ == 'DiGraph':
                real_edge += G.out_edges[edge[0], edge[1]]['weight']
                total_edge += G.out_edges[edge[0], edge[1]]['weight']
                if G.has_edge(edge[1], edge[0]):
                    total_edge += G.out_edges[edge[1], edge[0]]['weight']
                
                if option == 'remove':
                    if total_edge < threshold:
                        edge_to_delete.append((edge[0], edge[1]))
                        if G.has_edge(edge[1], edge[0]) and edge[0] != edge[1]:
                            edge_to_delete.append((edge[1], edge[0]))
                    total_edge = 0
            else:
                if option == 'remove':
                    if edge[2]['weight'] < threshold:
                        edge_to_delete.append((edge[0], edge[1]))
                else:
                    total_edge += edge[2]['weight']

        if option == 'remove':
            for edge in edge_to_delete:
                try:
                    G.remove_edge(*edge)
                except:
                    pass
            if type(G).__name__ == 'DiGraph':
                largest_cc = max(nx.weakly_connected_components(G), key=len)
            else:
                largest_cc = max(nx.connected_components(G), key=len)

            G = G.subgraph(largest_cc).copy()
            return G
        else:
            if type(G).__name__ == 'DiGraph':
                return real_edge
            else:
                return total_edge
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
        if G.has_edge(source, destination):
            G[source][destination]['weight'] += 1.0
        else:
            G.add_edge(source, destination, weight = 1.0)
    return G

def manage_and_save(graphs, path):

    for graph in graphs: 

        name = 'Final_'+type(graph).__name__   
        suffix = ''     
        if 'vax' in graph.name:
            threshold = 1
            name = name + '_Vax'
            suffix = '_Vax.gml'
        else:
            threshold = 3
            name = name + '_Covid'
            suffix = '_Covid.gml'

        name = name + '.gml'

        print(nx.info(graph))
        print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(graph, 'count')))
        print()

        graph = nodes_management(graph, 'remove', threshold)
        graph.name = graph.name.replace('Starter', 'Final')
        print(nx.info(graph))
        print("{:<20}{:<8}".format('Real number of Edges: ', nodes_management(graph, 'count')))
        print()
        if 'Direct' not in graph.name:
            G_multi = nx.MultiGraph()
            G_multi = create_multi_graph(graph)
            G_multi.name = f'Final_MultiGraph{suffix}'
            nx.write_gml(G_multi, path + '/Graph/' + G_multi.name)
            print(nx.info(G_multi))
            print()        

        nx.write_gml(graph, f'{path}/Graph/{name}')

def create_multi_graph(G):
    G_multi = nx.MultiGraph()
    G_multi.name = 'Final multi ' + G.name.split('graph')[-1]

    for edge in G.edges(data = True):
        weight = edge[2]['weight']
        for _ in range(int(weight)):
            G_multi.add_edge(edge[0], edge[1])
    
    return G_multi

def delete_url(tweet):
    for i in range(len(tweet)):
        tweet[i] = re.sub(r'\b(http:|www\.)(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r"http\S+", '', tweet[i])
        tweet[i] = re.sub(r'http:\\*/\\*/.*?\s', '', tweet[i])
        tweet[i] = re.sub(r'https:\\*/\\*/.*?\s', '', tweet[i])
        tweet[i] = re.sub(r"twitter.(\w+)", ' ', tweet[i], flags=re.MULTILINE)
        tweet[i] = re.sub(r'://(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r"://", ' ', tweet[i], flags=re.MULTILINE)
        tweet[i] = re.sub(r"/(\w+)", ' ', tweet[i], flags=re.MULTILINE)
        tweet[i] = re.sub(r"#", '', tweet[i])
        tweet[i] = re.sub(r'陈秋实(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'full(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'utm_source(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'utm_medium=(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'=social(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'=web&(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'utm_campaign(?:[^\s,.!?]|[,.!?](?!\s))+', '', tweet[i])
        tweet[i] = re.sub(r'.html', '', tweet[i])
    return tweet

def plot_line(x_values, y_values, title, x_text, y_text, legend):
    
    x_values = pd.Series(data=x_values)
    y_values = pd.Series(data=y_values)
    
    fig, ax = plt.subplots(figsize=(15, 10))
    fig.set_size_inches(22,8)
    ax.set_xticks(x_values)
    ax.plot(x_values, y_values, color='black', marker='o', label = legend)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(x_text)
    ax.set_ylabel(y_text)
    save_img(title)
    plt.show()
    
def save_img(title):    
    plt.savefig('./analysis_image/'+title+'.png', dpi = 300, quality = 95, format = 'png', pad_inches = 1000)