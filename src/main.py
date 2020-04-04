from preprocessing.ops_on_raw_data import ops_on_corona, ops_on_vac

def preprocessing_operation():
    ops_on_corona()
    ops_on_vac()
    print("PREPROCESSING DONE")

if __name__ == '__main__':
    preprocessing_operation()



