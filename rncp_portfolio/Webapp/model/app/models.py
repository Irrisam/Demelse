import numpy as np
from db_tools import db_user_fetcher
from failsafes import get_failsafes
from model_cache import model_cache_checker
from sklearn.metrics import pairwise_distances
from similarity import compute_mission_scores
import traceback
from exceptions import IdError


def recommend(user_id, dataset_path, data_type):
    try:
        # Model cache handling
        data, cosine_sim = model_cache_checker(dataset_path)
        print(
            f"Dataset loaded with {len(data)} users\n")

        # Fetch user data from DB
        user_data = db_user_fetcher(user_id, data_type)
        # Data quaity checker and failsafe values
        user_data = get_failsafes(
            user_data, data_type)
        print("Cleaned user data:", user_data)
        print('\n')

        # Find user index
        idx_list = data.index[data['user_id'] == user_id].tolist()
        if not idx_list:  # Unfound user handling
            return {f"ID {user_id} was not found in the database or was written incorrectly (recommend)"}
        idx = idx_list[0]
        # Sort missions by score
        sorted_categories = compute_mission_scores(idx, data, cosine_sim)
        return sorted_categories
    except IndexError as e:
        traceback.print_exc(limit=1)
        raise IdError(
            f'ID {user_id} was not found in the database or was written incorrectly')
    except Exception as e:
        print("An untracked error occurred:", type(e).__name__, "–", e)
        traceback.print_exc(limit=1)
        return None
