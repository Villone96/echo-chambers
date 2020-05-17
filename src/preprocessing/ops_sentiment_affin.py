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



def add_sentiment():
    nltk.download('punkt')
    nltk.download('stopwords')
    covid()
    vax()

def get_stopword():
    with open("./preprocessing/stopwords_affin.txt", "rb") as fp:
        stop_words = pickle.load(fp)
    return stop_words

def add_sent_weight(DiGraph, CompGraph, stop_words, name):
    total_tweet = 0
    punctuation = string.punctuation
    afinn = Afinn()
    max_val = 0
    min_val = 0
    score = 0
    no_node = 0
    for node in tqdm(DiGraph.nodes(), desc='node processed'):
        tweet = list()
        total_pers_tweet = 0
        info = DiGraph.out_edges(node, data=True)
        for edge in info:
            if isinstance(edge[2]['tweets'], (str)):
                edge[2]['tweets'] = [edge[2]['tweets']]
            tweet.append(list(edge)[2]['tweets'])
            total_pers_tweet += list(edge)[2]['weight']
        tweet = [item for sublist in tweet for item in sublist]
        total_tweet += total_pers_tweet
        
        if len(tweet) != total_pers_tweet:
            print(f'{node} presents {len(tweet)} but they are {total_pers_tweet}')
            break
            
        for i in range(len(tweet)):
            tweet[i] = re.sub(r"#(\w+)", ' ', tweet[i], flags=re.MULTILINE)
            tweet[i] = re.sub(r"@(\w+)", ' ', tweet[i], flags=re.MULTILINE)
            tweet[i] = re.sub(r"www.(\w+)", ' ', tweet[i], flags=re.MULTILINE)
            tweet[i] = re.sub(r"twitter.(\w+)", ' ', tweet[i], flags=re.MULTILINE)
            tweet[i] = re.sub(r"(\w+)-(\w+).html", ' ', tweet[i], flags=re.MULTILINE)
            tweet[i] = re.sub(r"(\w+)-(\w+)-(\w+)", ' ', tweet[i], flags=re.MULTILINE)
            tweet[i] = re.sub(r"(\w+)_(\w+)_(\w+)", ' ', tweet[i], flags=re.MULTILINE)

        tweet_series = pd.Series(tweet)
        
        tokening = TweetTokenizer(strip_handles=True, reduce_len=True)
        tweets_tokenized = tweet_series.apply(tokening.tokenize)
        for sentence in range(len(tweets_tokenized)):
            not_urls = [token for token in tweets_tokenized[sentence] if 'http' not in token]
            not_number = [token for token in not_urls if not token.isdigit()]
            tweets_tokenized[sentence] = not_number
        
        tweets_tokenized_stop = tweets_tokenized.apply(lambda x: [item for item in x if item not in stop_words])
        tweets_tokenized_stop_punct = tweets_tokenized_stop.apply(lambda x: [item for item in x if item not in punctuation])
        tweets_tokenized_final = tweets_tokenized_stop_punct.apply(lambda x: [item for item in x if item not in stop_words])
        
        list_done = list(tweets_tokenized_final)
        sentence = ""
        final_score = list()
        for tweet in list_done:
            for word in tweet:
                sentence += f'{word} '
            final_score.append(afinn.score(sentence))
            sentence = ''
            
        if len(final_score) == 0:
            DiGraph.nodes[node]['sentiment'] = 0
            CompGraph.nodes[node]['sentiment'] = 0
        else:
            affin_score = sum(final_score)/len(final_score)
            DiGraph.nodes[node]['sentiment'] = affin_score
            CompGraph.nodes[node]['sentiment'] = affin_score
            if max_val == 0:
                max_val = affin_score
            elif max_val < affin_score:
                max_val = affin_score

            if min_val == 0:
                min_val = affin_score
            elif min_val > affin_score:
                min_val = affin_score

    new_max = 10
    new_min = -10
    old_range = max_val - min_val
    new_range = new_max - new_min

    for node in DiGraph.nodes():
        old_value = DiGraph.nodes[node]['sentiment']
        if old_value != 0:
            new_value = (((old_value - min_val)*new_range)/old_range)+new_min
            DiGraph.nodes[node]['sentiment'] = new_value
            CompGraph.nodes[node]['sentiment'] = new_value

    for edge in CompGraph.edges(data=True):
        sentiment_diff = 10 - abs(CompGraph.nodes[edge[0]]['sentiment'] - CompGraph.nodes[edge[1]]['sentiment'])
        CompGraph[edge[0]][edge[1]]['weightWithSentiment'] = CompGraph[edge[0]][edge[1]]['weight'] + sentiment_diff

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