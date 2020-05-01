from preprocessing.ops_on_raw_data import ops_on_corona, ops_on_vac
from preprocessing.ops_build_graph import graph_ops
from community.community_detection import start_community_detection

def preprocessing_operation():
    ops_on_corona()
    ops_on_vac()
    graph_ops()
    print("PREPROCESSING DONE")
    print("")

def community_detection():
    start_community_detection()

if __name__ == '__main__':
    preprocessing_operation()
    #community_detection()



