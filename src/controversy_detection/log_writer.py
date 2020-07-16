import logging
import networkx as nx

def log_write_start_end(start, data_name = ''):
    logging.basicConfig(filename='controversy_detection.log', level=logging.INFO, format='%(message)s')
    if start:
        print(data_name)
        logging.info(f'--------------------{data_name}--------------------')
    else:
        if data_name == 'Covid':
            logging.info(f'---------------------------------------------------------')
        else:
            logging.info(f'------------------------------------------------------')