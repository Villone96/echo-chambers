import os
import nltk
from afinn import Afinn
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from collections import Counter
import itertools
from nltk.corpus import stopwords
import string
from nltk import wordpunct_tokenize
from nltk.stem.lancaster import LancasterStemmer
import networkx as nx
from tqdm import tqdm
import re 
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from preprocessing.utilities import delete_url



def add_sentiment():
    nltk.download('punkt')
    nltk.download('stopwords')
    covid()
    vax()

def get_stopword():
    with open("./preprocessing/stopwords_vader.txt", "rb") as fp:
        stop_words = pickle.load(fp)
    return stop_words

def add_sent_weight(DiGraph, CompGraph, stop_words, name):
    total_tweet = 0
    max_val = 0
    min_val = 0
    score = 0
    no_node = 0
    analyser = SentimentIntensityAnalyzer()
    tokening = TweetTokenizer(strip_handles=True, reduce_len=True)
    max_n_edge = 0
    min_n_edge = 0

    total_possible_edges = list()

    for node in tqdm(DiGraph.nodes(), desc='node processed'):
        tweet = list()
        total_pers_tweet = 0
        info = DiGraph.out_edges(node, data=True)
        for edge in info:
            if edge[0] != edge[1]:
                weight = edge[2]['weight']
                total_possible_edges.append(weight)
                if max_n_edge == 0:
                    max_n_edge = weight
                    min_n_edge = weight
                if max_n_edge < weight:
                    max_n_edge = weight
                if min_n_edge > weight:
                    min_n_edge = weight


            if isinstance(edge[2]['tweets'], (str)):
                edge[2]['tweets'] = [edge[2]['tweets']]
            tweet.append(list(edge)[2]['tweets'])
            total_pers_tweet += list(edge)[2]['weight']
        tweet = [item for sublist in tweet for item in sublist]
        total_tweet += total_pers_tweet

        if len(tweet) != total_pers_tweet:
            print(f'{node} presents {len(tweet)} but they are {total_pers_tweet}')
            break
    
        tweet = set(tweet)
        tweet = list(tweet)

        tweet = delete_url(tweet)
            
        tweets_series = pd.Series(tweet)
        tweets_tokenized = tweets_series.apply(tokening.tokenize)
        for sentence in range(len(tweets_tokenized)):
            not_number = [token for token in tweets_tokenized[sentence] if not token.isdigit()]
            tweets_tokenized[sentence] = not_number
            
        tweets_tokenized_stop = tweets_tokenized.apply(lambda x: [item for item in x if item not in stop_words])
        list_done = list(tweets_tokenized_stop)
        final_score = list()

        sentence = ''
        for tweet in list_done:
            for word in tweet:
                sentence += f'{word} '

            vader_score = analyser.polarity_scores(sentence)
            final_score.append(vader_score['compound'])
            sentence = '' 

        if len(final_score) == 0:
            DiGraph.nodes[node]['sentiment'] = 0
            CompGraph.nodes[node]['sentiment'] = 0
        else:
            vader_score = sum(final_score)/len(final_score)
            DiGraph.nodes[node]['sentiment'] = vader_score
            CompGraph.nodes[node]['sentiment'] = vader_score

            if max_val == 0:
                max_val = vader_score
            elif max_val < vader_score:
                max_val = vader_score

            if min_val == 0:
                min_val = vader_score
            elif min_val > vader_score:
                min_val = vader_score
    new_max_edge = int((((max_n_edge*np.median(total_possible_edges))/np.mean(total_possible_edges))/2) - np.mean(total_possible_edges))
    new_min_edge = 1
    print(f'VALGO: {new_max_edge}')

    new_max = int(new_max_edge*0.1)
    new_min = -new_max
    old_range = max_val - min_val
    new_range = new_max - new_min


    for node in DiGraph.nodes():
        old_value = DiGraph.nodes[node]['sentiment']
        if old_value != 0:
            new_value = (((old_value - min_val)*new_range)/old_range)+new_min
            DiGraph.nodes[node]['sentiment'] = new_value
            CompGraph.nodes[node]['sentiment'] = new_value


    #print(max_n_edge)
    #print(min_n_edge)
    #print(np.mean(total_possible_edges))
    #print(np.median(total_possible_edges))
    old_range = max_n_edge - min_n_edge
    new_range = new_max_edge - new_min_edge

    for edge in CompGraph.edges(data=True):
        old_value = edge[2]['weight']
        new_value = (((old_value - min_n_edge)*new_range)/old_range)+new_min_edge
        CompGraph[edge[0]][edge[1]]['weightWithSentiment'] = new_value

    for edge in CompGraph.edges(data=True):
        sentiment_diff = new_max*2 - abs(CompGraph.nodes[edge[0]]['sentiment'] - CompGraph.nodes[edge[1]]['sentiment'])
        if CompGraph[edge[0]][edge[1]]['weightWithSentiment'] + sentiment_diff >= 1:
            CompGraph[edge[0]][edge[1]]['weightWithSentiment'] = CompGraph[edge[0]][edge[1]]['weightWithSentiment'] + sentiment_diff
        else:
            CompGraph[edge[0]][edge[1]]['weightWithSentiment'] = 1

    nx.write_gml(CompGraph, f'Final_Graph_{name}.gml')
    nx.write_gml(DiGraph, f'Final_DiGraph_{name}.gml')


def covid():
    starting_path = os.getcwd()
    stop_words = get_stopword()
    path = os.path.join(starting_path, 'data/corona_virus/Graph')
    os.chdir(os.path.join(path))

    CompGraph = nx.read_gml('Final_Graph_Covid.gml')
    # if not 'weightWithSentiment' in list(CompGraph.edges(data=True))[0][2]:
    print(nx.info(CompGraph))
    print()
    DiGraph = nx.read_gml('Final_DiGraph_Covid.gml')
    print(nx.info(DiGraph))
    print()
    add_sent_weight(DiGraph, CompGraph, stop_words, 'Covid')

    os.chdir(starting_path)

def vax():
    starting_path = os.getcwd()
    stop_words = get_stopword()
    path = os.path.join(starting_path, 'data/vax_no_vax/Graph')
    os.chdir(os.path.join(path))

    CompGraph = nx.read_gml('Final_Graph_Vax.gml')
    if not 'weightWithSentiment' in list(CompGraph.edges(data=True))[0][2]:
        print(nx.info(CompGraph))
        print()
        DiGraph = nx.read_gml('Final_DiGraph_Vax.gml')
        print(nx.info(DiGraph))
        print()
        add_sent_weight(DiGraph, CompGraph, stop_words, 'Vax')

    os.chdir(starting_path)