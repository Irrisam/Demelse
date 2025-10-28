import pandas as pd
import numpy as np
from db_tools import db_user_fetcher
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
from file_system_tools import fs_file_opener
import os
from joblib import load, dump
import traceback
from exceptions import IdError


def recommend(user_id, dataset_path, data_type):
    try:
        cache_path = "trained_models/" + dataset_path.replace(
            ".csv", "_cosine.joblib")
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
        user_data = db_user_fetcher(user_id, data_type)

        service_failsafe = [('urgences', 0.0), ('reanimation', 0.0), ('bloc_op', 0.0), ('medecine_interne', 0.0), ('biology', 0.0), ('unite_de_soin', 0.0),
                            ('ssr', 0.0), ('chirurgie', 0.0), ('endocrino', 0.0), ('medecine_specialite', 0.0), ('geriatrie', 0.0), ('medecine_generale', 0.0)]
        etab_failsafe = [('hea_cen', 0.0), ('hea_hou', 0.0), ('ssr', 0.0), ('had', 0.0), ('home_consult', 0.0), ('teleconsult', 0.0),
                         ('labo', 0.0), ('priv_comp', 0.0), ('ehpad_rh', 0.0), ('other_ms', 0.0), ('clinic', 0.0), ('hospi', 0.0)]
        rythme_failsafe = [('DAY', 0.0), ('NIGHT', 0.0), ]
        if user_data.empty:

            if data_type == 'USER_ETAB' or data_type == 'CONTENT_ETAB':
                return (etab_failsafe)
            if data_type == 'USER_SERVICE' or data_type == 'CONTENT_SERVICE':
                return (service_failsafe)
            if data_type == 'CONTENT_RYTHME':
                return (rythme_failsafe)

        idx_list = data.index[data['user_id'] == user_id].tolist()
        print('la')
        print(idx_list)
        if not idx_list:
            return {f"ID {user_id} was not found in the database or was written incorrectly (recommend)"}
        print('pas la')
        idx = idx_list[0]

        user_choices = data.iloc[idx, 1:]

        available_missions = data.columns[1:]

        similar_users_idx = cosine_sim[idx].argsort()[::-1]

        mission_scores = {}

        for user_idx in similar_users_idx:
            if user_idx == idx:
                continue

            user_choices_sim = data.iloc[user_idx, 1:]

            X = np.array(user_choices[available_missions]).reshape(1, -1)
            Y = np.array(user_choices_sim[available_missions]).reshape(1, -1)

            jaccard_sim = 1 - pairwise_distances(X, Y, metric='hamming')[0][0]

            for mission in available_missions:
                if user_choices[mission] != user_choices_sim[mission]:
                    mission_scores[mission] = mission_scores.get(
                        mission, 0) + jaccard_sim * user_choices_sim[mission]

        if not mission_scores:
            print('No score to return')
            return None
        sorted_categories = sorted(
            mission_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_categories
    except IndexError as e:
        traceback.print_exc(limit=1)
        raise IdError(
            f'ID {user_id} was not found in the database or was written incorrectly')
    except Exception as e:
        print("An untracked error occurred:", type(e).__name__, "–", e)
        traceback.print_exc(limit=1)
        return None
