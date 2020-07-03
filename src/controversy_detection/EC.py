from scipy.sparse import coo_matrix
import numpy as np
import networkx as nx
from tqdm import tqdm
import math
from controversy_detection.GMCK import lists_to_dict
import logging


def force_atlas2_layout(graph, atlas_properties):

        print("Start creating Force Atlas Layout")
        iterations = atlas_properties.get("iterations", 1000)
        linlog = atlas_properties.get("linlog", False)
        pos = atlas_properties.get("pos", None)
        nohubs = atlas_properties.get("nohubs", False)
        k = atlas_properties.get("k", None)
        dim = atlas_properties.get("dim", 2)

        A = nx.to_scipy_sparse_matrix(graph, dtype='f')
        nnodes, _ = A.shape

        try:
            A = A.tolil()
        except Exception as e:
            A = (coo_matrix(A)).tolil()
        if pos is None:
            pos = np.asarray(np.random.random((nnodes, dim)), dtype=A.dtype)
        else:
            pos = pos.astype(A.dtype)
        if k is None:
            k = np.sqrt(1.0 / nnodes)
        t = 0.1

        dt = t / float(iterations + 1)
        displacement = np.zeros((dim, nnodes))
        for _ in tqdm(range(iterations)):
            displacement *= 0
            for i in range(A.shape[0]):
                delta = (pos[i] - pos).T
                distance = np.sqrt((delta ** 2).sum(axis=0))
                distance = np.where(distance < 0.01, 0.01, distance)
                Ai = np.asarray(A.getrowview(i).toarray())
                dist = k * k / distance ** 2
                if nohubs:
                    dist = dist / float(Ai.sum(axis=1) + 1)
                if linlog:
                    dist = np.log(dist + 1)
                displacement[:, i] += \
                    (delta * (dist - Ai * distance / k)).sum(axis=1)
            length = np.sqrt((displacement ** 2).sum(axis=0))
            length = np.where(length < 0.01, 0.01, length)
            pos += (displacement * t / length).T
            t -= dt

        print("Force Atlas done")
        return dict(zip(graph, pos))
    
    
def get_distance(point_a, point_b):
    x1 = point_a[0]
    y1 = point_a[1]
    x2 = point_b[0]
    y2 = point_b[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def start_EC(graph, com_type, iterations=1000):
    logging.basicConfig(filename='controversy_detection.log', level=logging.INFO, format='%(message)s')
    left = list()
    right = list()

    for node in graph.nodes(data=True):
        if node[1][com_type] == 0:
            left.append(node[0])
        else:
            right.append(node[0])
            
    dict_left = lists_to_dict(left, [1] * len(left))
    dict_right = lists_to_dict(right, [1] * len(right))
    atlas_properties = {"iterations": iterations, "linlog": False, "pos": None, "nohubs": False, "k": None, "dim": 2}
    position_node = force_atlas2_layout(graph, atlas_properties)
    atlas_layout = position_node
    dict_positions = {}
    for i in atlas_layout:
        node = i
        line1 = atlas_layout[i]
        [x, y] = [line1[0], line1[1]]
        dict_positions[node] = [x, y]

    left_list = list(dict_left.keys())
    total_lib_lib = 0.0
    count_lib_lib = 0.0

    for i in tqdm(range(len(left_list))):
        user1 = left_list[i]
        for j in range(i + 1, len(left_list)):
            user2 = left_list[j]
            dist = get_distance(dict_positions[user1], dict_positions[user2])
            total_lib_lib += dist
            count_lib_lib += 1.0
    avg_lib_lib = total_lib_lib / count_lib_lib
    right_list = list(dict_right.keys())
    total_cons_cons = 0.0
    count_cons_cons = 0.0

    for i in tqdm(range(len(right_list))):
        user1 = right_list[i]
        for j in range(i + 1, len(right_list)):
            user2 = right_list[j]
            dist = get_distance(dict_positions[user1], dict_positions[user2])
            total_cons_cons += dist
            count_cons_cons += 1.0
    avg_cons_cons = total_cons_cons / count_cons_cons

    total_both = 0.0
    count_both = 0.0

    for i in tqdm(range(len(left_list))):
        user1 = left_list[i]
        for j in range(len(right_list)):
            user2 = right_list[j]
            dist = get_distance(dict_positions[user1], dict_positions[user2])
            total_both += dist
            count_both += 1.0
    avg_both = total_both / count_both

    score = round(1 - ((avg_lib_lib + avg_cons_cons) / (2 * avg_both)), 4)
    print("Embedding score: {}".format(score))
    logging.info(f'Embedding score: {score}')
    logging.info('\n')