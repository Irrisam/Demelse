import os
from joblib import load, dump
import pandas as pd
from file_system_tools import fs_file_opener
from sklearn.metrics.pairwise import cosine_similarity


def model_cache_checker(dataset_path):
    cache_path = "trained_models/" + \
        dataset_path.replace('.csv', '_cosine.joblib')
    if os.path.exists(cache_path):
        print("Loading model from cache")
        data, cosine_sim = load(cache_path)
    else:
        print('Training model')
        data = fs_file_opener(dataset_path)
        data.reset_index(drop=True, inplace=True)

        data = data.map(lambda x: str(x).replace(' ', ''))
        data = data.apply(pd.to_numeric, errors='coerce')
        data.dropna(inplace=True)

        data['user_id'] = data['user_id'].astype(int)
        cosine_sim = cosine_similarity(data.iloc[:, 1:])
        print('Saving model')
        dump((data, cosine_sim), cache_path)

    return data, cosine_sim
