from itertools import product
from models import recommend
import numpy as np


def value_getter(user_id, data_type='full', dominant_category_check=False):
    # gathers data in lists from the models per user and returns a list of tuples containing the unique category and its score post sum
    if data_type == 'ETAB':
        data_categories = [['ETAB', 'USER'], ['ETAB', 'CONTENT']]
    if data_type == 'SERVICE':
        data_categories = [['SERVICE', 'USER'], ['SERVICE', 'CONTENT']]
    if data_type == 'RYTHME':
        data_categories = [['RYTHME', 'CONTENT']]
    if data_type == 'full':
        data_categories = [['ETAB', 'USER'], ['ETAB', 'CONTENT'], [
            'SERVICE', 'USER'], ['SERVICE', 'CONTENT'], ['RYTHME', 'CONTENT']]
    score_values = []
    dominant_recommendation_scores = {'user_score': 0, 'content_score': 0}
    for recommendation_type in range(len(data_categories)):
        dataset_path = 'trained_models_{}_{}_TRAINING.csv'.format(
            data_categories[recommendation_type][1], data_categories[recommendation_type][0])
        data_type_fetch = str(
            data_categories[recommendation_type][1]) + '_' + str(data_categories[recommendation_type][0])
        recommended_results = recommend(user_id, dataset_path, data_type_fetch)
        for iteration in range(len(recommended_results)):
            score = recommended_results[iteration][1]
            if dominant_category_check:
                if data_categories[recommendation_type][1] == 'CONTENT':
                    dominant_recommendation_scores['content_score'] += score
                elif data_categories[recommendation_type][1] == 'USER':
                    dominant_recommendation_scores['user_score'] += score
            score_values.append(recommended_results)

    aggregated_scores = {}
    for reco_list in score_values:
        for item_name, score in reco_list:
            if isinstance(score, np.ndarray):
                score = score.sum()
            if item_name == 'clinic':
                score = score / 4
            if item_name in aggregated_scores:
                aggregated_scores[item_name] += score * 3
            else:
                aggregated_scores[item_name] = score

    summed_up_scores_list = [(key, value)
                             for key, value in aggregated_scores.items()]
    return (summed_up_scores_list)


def generate_top_combinations(user_id, result_limit=50, dominant_category_check=False):
    # generates a list of typo trios and returns them ordered by grouped value DESC
    # orderded by ETAB, SERVICE, RYTHME
    results = {
        'ETAB': value_getter(user_id, 'ETAB', dominant_category_check),
        'SERVICE': value_getter(user_id, 'SERVICE', dominant_category_check),
        'RYTHME': value_getter(user_id, 'RYTHME', dominant_category_check)
    }
    etab_scores = results['ETAB']
    service_scores = results['SERVICE']
    rythme_scores = results['RYTHME']

    all_combinations = product(etab_scores, service_scores, rythme_scores)
    combination_scores = []

    for combination in all_combinations:
        if len(combination_scores) == result_limit:
            break

        scores = [item[1] for item in combination]
        total_score = sum(scores)
        if dominant_category_check:
            highest_score_index = scores.index(max(scores))
            block = ['ETAB', 'SERVICE', 'RYTHME'][highest_score_index]
            combination_scores.append((combination, total_score, block))
        else:
            combination_scores.append((combination, total_score))

    sorted_combinations = sorted(
        combination_scores, key=lambda x: x[1], reverse=True)

    top_combinations = sorted_combinations[:result_limit]

    return sorted_combinations, top_combinations


def mission_trios_selector(user_id, result_limit, trio_index, dominant_category_check=False):
    # selects the {trio_index} trio of missions and returns the category names in a list
    try:
        returned_score_trios, full_trios = generate_top_combinations(
            user_id, result_limit, dominant_category_check)
        selected_score_trios = returned_score_trios[trio_index]
        selected_trio = []
        for index in range(len(selected_score_trios[0])):
            selected_trio.append(selected_score_trios[0][index][0])
    except IndexError:
        raise IndexError('Selected index out of range')
    return selected_trio, full_trios
