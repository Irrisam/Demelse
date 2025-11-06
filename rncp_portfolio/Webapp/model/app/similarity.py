import numpy as np
from sklearn.metrics import pairwise_distances


def compute_mission_scores(idx, data, cosine_sim):
    # Get user datas
    user_choices = data.iloc[idx, 1:]
    available_missions = data.columns[1:]

    # Sort similar users by cosine
    similar_users_idx = cosine_sim[idx].argsort()[::-1]
    mission_scores = {}

    for user_idx in similar_users_idx:
        if user_idx == idx:
            continue

        user_choices_sim = data.iloc[user_idx, 1:]

        # Jaccard similarity
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

    return sorted(mission_scores.items(), key=lambda x: x[1], reverse=True)
