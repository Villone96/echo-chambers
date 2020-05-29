import pickle
import gensim
from tqdm import tqdm
import networkx as nx

from preprocessing.utilities import clean_data

def assign_topic_weight(DiGraph, CompGraph, name, lda_model_mallet):
    lda_model = gensim.models.wrappers.ldamallet.malletmodel2ldamodel(lda_model_mallet)
    dictionary = lda_model.__dict__['id2word']  

    all_topics = dict()
    for node in tqdm(DiGraph.nodes()):
        info = DiGraph.out_edges(node, data=True)
        tweet = list()
        for edge in info:
            if isinstance(edge[2]['tweets'], (str)):
                edge[2]['tweets'] = [edge[2]['tweets']]
            tweet.append(list(edge)[2]['tweets'])
        tweets = [item for sublist in tweet for item in sublist]
        processed_docs = clean_data(tweets)
        clean = list()
        for i in range(len(processed_docs)):
            for tweet in [processed_docs[i]]:
                sentence = ''
                for word in tweet:
                    sentence += f'{word} '
                clean.append(sentence)
                clean[i] = clean[i].strip().split()

        sum_score = 0       
        user_topics = set()
        for sentence in clean:
            # print(sentence)
            sentence = dictionary.doc2bow(sentence)
            # print(sentence)
            topic_id = sorted(lda_model[sentence], key=lambda tup: -1*tup[1])[0][0]
            user_topics.add(topic_id)
            if topic_id in all_topics:
                all_topics[topic_id] += 1
            else:
                all_topics[topic_id] = 1
            # print(sorted(lda_model[sentence], key=lambda tup: -1*tup[1])[0][0])
            # print(sorted(lda_model[sentence], key=lambda tup: -1*tup[1])[1][0])
            # print(sorted(lda_model[sentence], key=lambda tup: -1*tup[1])[3][0])
            # print()
        # print(user_topics)
        # print()
        
        DiGraph.nodes[node]['tweetTopic'] = user_topics
        CompGraph.nodes[node]['tweetTopic'] = user_topics

    for edge in CompGraph.edges(data=True):
        topic_diff = 30 - len(CompGraph.nodes[edge[0]]['tweetTopic'] ^ CompGraph.nodes[edge[1]]['tweetTopic'])        
        CompGraph[edge[0]][edge[1]]['TopicDiff'] = topic_diff*2     
    
    for edge in CompGraph.edges(data=True):
        sentiment_diff = 60 - abs(CompGraph.nodes[edge[0]]['sentiment'] - CompGraph.nodes[edge[1]]['sentiment'])
        weight_sample = edge[2]['weightWithSentiment'] - sentiment_diff
        CompGraph[edge[0]][edge[1]]['weightWithTopic'] = weight_sample + edge[2]['TopicDiff']
        CompGraph[edge[0]][edge[1]]['Hibrid'] = edge[2]['weightWithSentiment'] + edge[2]['TopicDiff']

    for node in CompGraph.nodes(data=True):
        CompGraph.nodes[node[0]]['tweetTopic'] = str(list(CompGraph.nodes[node[0]]['tweetTopic']))
        DiGraph.nodes[node[0]]['tweetTopic'] = str(list(DiGraph.nodes[node[0]]['tweetTopic']))


    nx.write_gml(CompGraph, f'./Graph/Final_Graph_{name}.gml')
    nx.write_gml(DiGraph, f'./Graph/Final_DiGraph_{name}.gml')