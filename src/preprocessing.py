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
        os.mkdir('group_data')
        os.chdir(os.path.join(path, 'raw_data'))
        raw_datas = [element for element in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), element))]

        january_datas = [dataset for dataset in raw_datas if '-01-' in dataset]
        february_datas = [dataset for dataset in raw_datas if '-02-' in dataset]
        march_datas = [dataset for dataset in raw_datas if '-03-' in dataset]

        final_january = pd.read_csv(os.path.join(os.getcwd(), january_datas[0]), usecols = ['username', 'favorites', 'retweets', 
        'language', '@mentions', 'geo', 'text_con_hashtag'])
        total_rows += final_january.shape[0]
        for dataset in january_datas[1:]:
            addition = pd.read_csv(os.path.join(os.getcwd(), dataset), usecols = ['username', 'favorites', 'retweets', 
            'language', '@mentions', 'geo', 'text_con_hashtag'])
            total_rows += addition.shape[0]
            final_january = final_january.append(addition, ignore_index=True)
        print("CHECK ROWS ALL JANUARY DATASET VS FINAL JANUARY DATASET")
        print(total_rows)
        print(final_january.shape[0])
        print()
        total_rows = 0

        final_february = pd.read_csv(os.path.join(os.getcwd(), february_datas[0]), usecols = ['username', 'favorites', 'retweets', 
        'language', '@mentions', 'geo', 'text_con_hashtag'])
        total_rows += final_february.shape[0]
        for dataset in february_datas[1:]:
            addition = pd.read_csv(os.path.join(os.getcwd(), dataset), usecols = ['username', 'favorites', 'retweets', 
            'language', '@mentions', 'geo', 'text_con_hashtag'])
            total_rows += addition.shape[0]
            final_february = final_february.append(addition, ignore_index=True)
        print("CHECK ROWS ALL FEBRUARY DATASET VS FINAL FEBRUARY DATASET")
        print(total_rows)
        print(final_february.shape[0])
        print()
        total_rows = 0

        final_march = pd.read_csv(os.path.join(os.getcwd(), march_datas[0]), usecols = ['username', 'favorites', 'retweets', 
        'language', '@mentions', 'geo', 'text_con_hashtag'])
        total_rows += final_march.shape[0]
        for dataset in march_datas[1:]:
            addition = pd.read_csv(os.path.join(os.getcwd(), dataset), usecols = ['username', 'favorites', 'retweets', 
            'language', '@mentions', 'geo', 'text_con_hashtag'])
            total_rows += addition.shape[0]
            final_march = final_march.append(addition, ignore_index=True)
        print("CHECK ROWS ALL MARCH DATASET VS FINAL MARCH DATASET")
        print(total_rows)
        print(final_march.shape[0])
        print()

        os.chdir(os.path.join(path, 'group_data'))

        final_january.to_csv('January_dataset.csv', encoding='utf-8', index=True)
        final_february.to_csv('February_dataset.csv', encoding='utf-8', index=True)
        final_march.to_csv('March_dataset.csv', encoding='utf-8', index=True)
    
    
def extract_only_en():
    pass
