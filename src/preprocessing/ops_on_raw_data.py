import os
import pandas as pd

def check_directory_absence(name, path):
    os.chdir(path)
    directories = os.listdir()
    if not name in directories:
        return True
    else:
        return False

def ops_on_corona():
    group_by_month_corona()
    extract_only_en()

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

        final_january = pd.read_csv(january_datas[0], usecols = ['username', 'favorites', 'retweets', 
        'language', '@mentions', 'geo', 'text_con_hashtag'])
        total_rows += final_january.shape[0]
        for dataset in january_datas[1:]:
            addition = pd.read_csv(dataset, usecols = ['username', 'favorites', 'retweets', 
            'language', '@mentions', 'geo', 'text_con_hashtag'])
            total_rows += addition.shape[0]
            final_january = final_january.append(addition, ignore_index=True)
        print("CHECK ROWS ALL JANUARY DATASET VS FINAL JANUARY DATASET")
        print(total_rows)
        print(final_january.shape[0])
        print()
        total_rows = 0

        final_february = pd.read_csv(february_datas[0], usecols = ['username', 'favorites', 'retweets', 
        'language', '@mentions', 'geo', 'text_con_hashtag'])
        total_rows += final_february.shape[0]
        for dataset in february_datas[1:]:
            addition = pd.read_csv(dataset, usecols = ['username', 'favorites', 'retweets', 
            'language', '@mentions', 'geo', 'text_con_hashtag'])
            total_rows += addition.shape[0]
            final_february = final_february.append(addition, ignore_index=True)
        print("CHECK ROWS ALL FEBRUARY DATASET VS FINAL FEBRUARY DATASET")
        print(total_rows)
        print(final_february.shape[0])
        print()
        total_rows = 0

        final_march = pd.read_csv(march_datas[0], usecols = ['username', 'favorites', 'retweets', 
        'language', '@mentions', 'geo', 'text_con_hashtag'])
        total_rows += final_march.shape[0]
        for dataset in march_datas[1:]:
            addition = pd.read_csv(dataset, usecols = ['username', 'favorites', 'retweets', 
            'language', '@mentions', 'geo', 'text_con_hashtag'])
            total_rows += addition.shape[0]
            final_march = final_march.append(addition, ignore_index=True)
        print("CHECK ROWS ALL MARCH DATASET VS FINAL MARCH DATASET")
        print(total_rows)
        print(final_march.shape[0])
        print()

        all_data = final_january.append(final_february.append(final_march, ignore_index=True), ignore_index=True)
        print("CHECK ROWS ALL DATASET VS FINAL DATASET")
        print(all_data.shape[0])
        print(final_january.shape[0] + final_february.shape[0] + final_march.shape[0])

        os.chdir(os.path.join(path, 'group_data'))

        final_january.to_csv('January_dataset.csv', encoding='utf-8', index=False)
        final_february.to_csv('February_dataset.csv', encoding='utf-8', index=False)
        final_march.to_csv('March_dataset.csv', encoding='utf-8', index=False)
        all_data.to_csv('All_data.csv', encoding='utf-8', index=False)

    os.chdir(starting_path)
    
def extract_only_en():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/corona_virus')
    if check_directory_absence('final_data', path):
        os.mkdir('final_data')
        os.chdir(os.path.join(path, 'group_data'))

        df =  pd.read_csv('All_data.csv')
        filt = df['language'] == 'en'
        df_only_en = df[filt]
        df_only_en.drop(columns=['language'], inplace=True)
        df_only_en['@mentions'] = df_only_en['@mentions'].fillna('self')
        print('ONLY EN TWITTER FINAL SHAPE')
        print(df_only_en.shape)
        print()

        os.chdir(os.path.join(path, 'final_data'))
        df_only_en.to_csv('Final_data.csv', encoding='utf-8', index=False)

    os.chdir(starting_path)

def ops_on_vac():
    refine_data()

def refine_data():
    starting_path = os.getcwd()
    path = os.path.join(starting_path, 'data/vax_no_vax')
    if check_directory_absence('final_data', path):
        os.mkdir('final_data')
        os.chdir(os.path.join(path, 'raw_data'))
        df = pd.read_csv('./full_data.csv', usecols=['date', 'username', 'replies_count', 'retweets_count',
                                                      'likes_count', 'hashtags', 'mentions', 'tweet'])
        os.chdir(os.path.join(path, 'final_data'))
        df.to_csv('Final_data.csv', encoding='utf-8', index=False)

        print('VACCINATION DATA FINAL SHAPE')
        print(df.shape)

    os.chdir(starting_path)

        


