import os
import pandas as pd

def check_directory_absence(name, path):
    os.chdir(path)
    directories = os.listdir()
    if not name in directories:
        return True
    else:
        return False

def group_by_month_corona():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus')
    if check_directory_absence('group_data', path):
        total_rows = 0
        # os.mkdir('group_data')
        os.chdir(os.path.join(path, 'raw_data'))
        raw_datas = [element for element in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), element))]
        january_datas = [dataset for dataset in raw_datas if '-01-' in dataset]
        february_datas = [dataset for dataset in raw_datas if '-02-' in dataset]
        march_datas = [dataset for dataset in raw_datas if '-03-' in dataset]
        # print(len(january_datas) + len(february_datas) + len(march_datas))
        final_january = pd.read_csv(os.path.join(os.getcwd(), january_datas[0]))
        for dataset in january_datas[1:]:
            addition = pd.read_csv(os.path.join(os.getcwd(), dataset))
            total_rows += addition.shape[0]
            print(addition.shape)

            final_january = final_january.append(addition, ignore_index=True)

        print(final_january.shape)
        print(total_rows)

    
    
def extract_only_en():
    pass
