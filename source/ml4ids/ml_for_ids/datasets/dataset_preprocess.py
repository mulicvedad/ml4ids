import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle


def dataset_cleanup(dataset, drop_columns=None):
    dataset = shuffle(dataset)

    print('Dataset shape: {}'.format(dataset.values.shape))

    dataset.replace([np.inf, -np.inf], np.nan)
    dataset.dropna(how='any', inplace=True)

    if drop_columns is not None:
        dataset.drop(drop_columns, axis=1)

    print('Dataset shape: {}'.format(dataset.values.shape))

    dataset = dataset.drop(dataset.std()[dataset.std() < .3].index.values, axis=1)
    dataset = dataset.drop(dataset.std()[dataset.std() > 1000].index.values, axis=1)

    print('Dataset shape: {}'.format(dataset.values.shape))

    # dataset.values[abs(dataset.values) == np.inf] = 0

    return dataset


# Feature extraction - later on
# test = SelectKBest(score_func=chi2, k=10)
def split_data(dataset, target_map_fun=None):
    ds_vals = dataset.values

    X = ds_vals[:, 0:-1]
    Y = ds_vals[:, -1]

    if target_map_fun:
        for k, v in enumerate(Y):
            Y[k] = target_map_fun(v)

    X = X.astype(float)
    Y = Y.astype(int)
    X[X == np.inf] = 0.0
    min_max_scaler = MinMaxScaler()
    X = min_max_scaler.fit_transform(X)

    return train_test_split(X, Y, test_size=0.2, random_state=42)
