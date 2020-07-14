import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
from nltk.tokenize import TweetTokenizer
import os
import networkx as nx
from preprocessing.utilities import delete_url, plot_line
from preprocessing.ops_topic_lda import assign_topic_weight
from nltk.stem import PorterStemmer 
import pandas as pd
from tqdm import tqdm
import pickle
from gensim.models import CoherenceModel
import matplotlib.pyplot as plt


def add_topic():
    pass
    #covid()
    #vax()

def stemming_opt(token):
    ps = PorterStemmer() 
    token = ps.stem(token)
    return token

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(stemming_opt(token))
    return result

def creat_LDA_model(name):
    CG = nx.read_gml(f'./Graph/Final_DiGraph_{name}.gml')
    print(nx.info(CG))
    tokening = TweetTokenizer(strip_handles=True, reduce_len=True)
    np.random.seed(2018)
    nltk.download('wordnet')

    all_tweet = list()
    for edge in CG.edges(data=True):
        if isinstance(edge[2]['tweets'], (str)):
            edge[2]['tweets'] = [edge[2]['tweets']]
        all_tweet.append(edge[2]['tweets'])
    all_tweet = [item for sublist in all_tweet for item in sublist]
    raw_tweets = set()
    for tweet in tqdm(all_tweet):
        raw_tweets.add(tweet)
    raw_tweets = list(raw_tweets)
    raw_tweets = delete_url(raw_tweets)

    with open("./preprocessing/stopwords.txt", "rb") as fp:
        stop_words = pickle.load(fp)

    tweet_series = pd.Series(raw_tweets)
    print('Series done')
    tweets_tokenized = tweet_series.apply(tokening.tokenize)
    print('Tokening done')
    tweets_tokenized_stop = tweets_tokenized.apply(lambda x: [item for item in x if item not in stop_words])
    print('Stopword done')
    list_done = list(tweets_tokenized_stop)
    print('List done')

    clean_tweet = list()
    for tweet in tqdm(list_done, desc='tweet recomposed'):
        sentence = ''
        for word in tweet:
            sentence += f'{word} '
        clean_tweet.append(sentence)
    df = pd.DataFrame(np.array(clean_tweet).reshape(len(clean_tweet),1), columns = ['Tweet'])
    processed_docs = df['Tweet'].map(preprocess)
    dictionary = gensim.corpora.Dictionary(processed_docs)
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    list_lem = list()
    list_words = list()
    for doc in tqdm(bow_corpus, desc='doc processed'):
        for i in range(len(doc)):
            list_words.append(dictionary[doc[i][0]])
        list_lem.append(list_words)
        list_words = []

    coherence = list()
    mallet_path = './data/mallet_lda/bin/mallet'

    for i in tqdm(range(2, 31)):
        lda_model = gensim.models.wrappers.LdaMallet(mallet_path, bow_corpus, num_topics=i, id2word=dictionary, workers=4)
        
        coherence_model_lda = CoherenceModel(model=lda_model, texts=list_lem, dictionary=dictionary, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        coherence.append(coherence_lda)
        
        print(f'With {i} topic, it has been recorded {coherence_lda} of coherence')

        lda_model.save(f'./LDA_model/lda_model_{i}.model')
    
    with open("./LDA_model/coherence.txt", "wb") as fp:
        pickle.dump(coherence, fp)

    plt.style.use('seaborn')
    y_values = coherence
    x_values = list(np.arange(2, 31))

    plot_line(x_values, y_values, f'Coherence per numero di topic - Dataset {name}', 'Numero Topic', 'Valore Coherence', 'Coherence')

    df = pd.DataFrame(columns = ['TOPIC', 'WORDS'])
    i = 0
    for idx, topic in model.print_topics(-1, 15):
        print('Topic: {} \nWords: {}'.format(idx, topic))
        topic = topic.replace('*', ' ').replace('+', ' ').replace('"', ' ').replace('.', '')
        topic = re.sub('[0-9]+', '', topic)
        topic = topic.replace(" ", ",")
        topic = topic.replace(",,,,,,", ",")
        topic = topic.replace(",,", "")
        df.loc[i] = [idx, topic]
        i += 1
        print()
    df.to_csv('./LDA_model/topic.csv', index=False)

def covid():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus/')
    os.chdir(os.path.join(path))
    list_of_file = os.listdir('./LDA_model')
    create_model = True
    for file in list_of_file:
        if file == 'lda_top_coherence.model':
            create_model = False

    if create_model:
        creat_LDA_model('Covid')
    
    lda_model = gensim.models.wrappers.LdaMallet.load("./LDA_model/lda_top_coherence.model")
    #for idx, topic in lda_model.print_topics(-1, 15):
    #    print('Topic: {} \nWords: {}'.format(idx, topic))
    
    
    CompGraph = nx.read_gml(f'./Graph/Final_Graph_Covid.gml')
    if not 'weightWithTopic' in list(CompGraph.edges(data=True))[0][2]:
        print(nx.info(CompGraph))
        print()
        DiGraph = nx.read_gml('./Graph/Final_DiGraph_Covid.gml')
        print(nx.info(DiGraph))
        print()
        assign_topic_weight(DiGraph, CompGraph, 'Covid', lda_model)

    os.chdir(starting_path)

def vax():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax')
    os.chdir(os.path.join(path))

    list_of_file = os.listdir('./LDA_model')
    create_model = True
    for file in list_of_file:
        if file == 'lda_top_coherence.model':
            create_model = False

    if create_model:
        creat_LDA_model('Vax')
        
    lda_model = gensim.models.wrappers.LdaMallet.load("./LDA_model/lda_top_coherence.model")
    #for idx, topic in lda_model.print_topics(-1, 15):
    #    print('Topic: {} \nWords: {}'.format(idx, topic))
    CompGraph = nx.read_gml(f'./Graph/Final_Graph_Vax.gml')
    if not 'weightWithTopic' in list(CompGraph.edges(data=True))[0][2]:
        print(nx.info(CompGraph))
        print()
        DiGraph = nx.read_gml('./Graph/Final_DiGraph_Vax.gml')
        print(nx.info(DiGraph))
        print()
        assign_topic_weight(DiGraph, CompGraph, 'Vax', lda_model)


    os.chdir(starting_path)