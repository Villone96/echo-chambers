import igraph as ig
import networkx as nx
from networkx.algorithms.community.quality import coverage 
import os
from tqdm import tqdm

def start_community_detection():
    garimella_graph()
    covid_graph()
    vax_graph()

def garimella_graph():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/garimella_data/Graph')
    os.chdir(path)
    list_of_graph = os.listdir(path)
    for graph in list_of_graph:
        name = graph
        if 'Multi' in name or 'mothers' in name: 
            pass
        else:
            print(f'{name} graph')
            graph = ig.Graph(directed=False)
            graph = graph.Read_GML(name)

            multi_graph = nx.read_gml('Multi_'+name)

            communities = graph.community_leading_eigenvector(weights='weight')
            print(f'Modularity value: {round(communities.modularity, 4)}')

            communities = list(communities)

            list_com_name = list()
            community_member = list()

            cont = 0

            for community in communities:
                for member in tqdm(community, desc=f'Community {cont} member processed: '):
                    community_member.append(graph.vs["label"][member])
                list_com_name.append(community_member)
                community_member = list()
                cont += 1

            list_com_name = [set(community) for community in list_com_name]
            print(f'Coverage value: {round(coverage(multi_graph, list_com_name), 4)}')
            print()





    os.chdir(starting_path)



def covid_graph():
    pass

def vax_graph():
    pass
    