import numpy as np
import pandas as pd


class MultiElementDelete(list):
    def __delitem__(self, key):
        if isinstance(key, (list, tuple)):
            for index in sorted(set(key), reverse=True):
                list.__delitem__(self, index)
        else:
            list.__delitem__(self, key)


def calc_data(dataset):
    """

    :param dataset: [[winner_name, win_score], [winner_name, win_score], ...]
                    winner_name in [player1, player2]
    :return: p1_score, p2_score
    """
    df = pd.DataFrame(dataset, columns=['winner', 'score'])
    sum_p1_score = df.groupby('winner').sum().loc['player1']['score']
    sum_p2_score = df.groupby('winner').sum().loc['player2']['score']

    p1_score = sum_p1_score - sum_p2_score
    p2_score = sum_p2_score - sum_p1_score

    return p1_score, p2_score
