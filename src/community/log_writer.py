import logging
import networkx as nx

def log_write_start_end(start, data_name = ''):
    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    if start:
        print(data_name)
        logging.info(f'--------------------{data_name}--------------------')
    else:
        if data_name == 'Covid':
            logging.info(f'---------------------------------------------------------')
        else:
            logging.info(f'------------------------------------------------------')

def log_write_graph_info(graph_name, info_graph, info_multi):
    print(f'{graph_name.upper()} GRAPH')
    print()
    print(info_graph)
    print()
    print(info_multi)
    print()

    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    logging.info(f'{graph_name.upper()} INFORMATION')
    logging.info(f'\n{info_graph}')
    logging.info(f'\n{info_multi}\n')
    

def log_write_com_result(alg, info_com, mod, cov, exe_time):
    print(f'{alg} modularity: {round(mod, 4)}')
    print(f'{alg} coverage: {round(cov, 4)}')
    print()

    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    logging.info(f'------{alg}------')
    logging.info(f'Community 0 length: {info_com[0]}')
    logging.info(f'Community 1 length: {info_com[1]}')
    logging.info(f'{alg} modularity: {round(mod, 4)}')
    logging.info(f'{alg} coverage: {round(cov, 4)}')
    logging.info(f'execution time: {round(exe_time, 4)}')
    if alg == 'Fluid':
        add_separator_space()

def add_separator_space():
    logging.basicConfig(filename='community_log.log', level=logging.INFO, format='%(message)s')
    logging.info(f'\n\n')
