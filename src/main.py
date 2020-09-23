from preprocessing.ops_on_raw_data import ops_on_corona, ops_on_vac
from preprocessing.ops_build_graph import graph_ops
from community.community_detection import start_community_detection
from preprocessing.topic_modelling import add_topic
from controversy_detection.start_controversy_detection import start_detection
from link_prediction.start_link_prediction import start_link_opt


import sys

def preprocessing_operation():
    ops_on_corona()
    ops_on_vac()
    graph_ops()
    print("PREPROCESSING DONE")
    print("")

def community_detection():
    start_community_detection()

def controversy_detection():
    start_detection()

def link_prediction():
    start_link_opt()

if __name__ == '__main__':
    preprocessing_operation()
    community_detection()
    controversy_detection()
    link_prediction()



