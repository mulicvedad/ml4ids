from enum import IntEnum

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle


class MissingDataResolutionStrategy(IntEnum):
    DROP_OBSERVATION = 1,
    DROP_FEATURE = 2,
    REPLACE_WITH_MEAN = 3


# @deprecated
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
def split_data(df, target_map_fun=None):
    ds_vals = df.values
    X, Y = split_data_and_labels_cols(ds_vals, target_map_fun)
    return train_test_split(X, Y, test_size=0.2, random_state=42)


def split_data_and_labels_cols(df, target_map_fun=None):
    data = df.values

    X = data[:, 0:-1]
    Y = data[:, -1]

    if target_map_fun:
        for k, v in enumerate(Y):
            Y[k] = target_map_fun(v)

    X = X.astype(float)
    Y = Y.astype(int)
    X[X == np.inf] = 0.0
    min_max_scaler = MinMaxScaler()
    X = min_max_scaler.fit_transform(X)

    return X, Y


def remove_non_numeric_cols(df):
    log(df, "Before handle non numeric cols")
    df = df.select_dtypes(include=np.number)
    log(df, "After handle non numeric cols")
    return df


def analyze_missing_data(df):
    log_missing_data_info(df)
    plot_missing_data_info(df)


def log_missing_data_info(df):
    for col in df.columns:
        pct_missing = np.mean(df[col].isnull())
        print('{} - {}%'.format(col, round(pct_missing * 100)))


def plot_missing_data_info(df):
    plot_missing_data_heatmap(df)
    plot_missing_data_histogram(df)


def plot_missing_data_heatmap(df):
    import seaborn as sns
    colours = ['#E27B65', '#50A372']  # Mark rows with missing data with red color, otherwise green
    sns.heatmap(df.isnull(), cmap=sns.color_palette(colours))


def plot_missing_data_histogram(df):
    for col in df.columns:
        missing = df[col].isnull()
        num_missing = np.sum(missing)

        if num_missing > 0:
            print('created missing indicator for: {}'.format(col))
            df['{}_ismissing'.format(col)] = missing

    # then based on the indicator, plot the histogram of missing values
    ismissing_cols = [col for col in df.columns if 'ismissing' in col]
    df['num_missing'] = df[ismissing_cols].sum(axis=1)
    df['num_missing'].value_counts().reset_index().sort_values(by='index').plot.bar(x='index', y='num_missing')


def handle_missing_data(df, strategy=MissingDataResolutionStrategy.DROP_OBSERVATION):
    log(df, "Before handle missing data")

    df.replace([np.inf, -np.inf], np.nan)

    if strategy == MissingDataResolutionStrategy.DROP_OBSERVATION:
        df.dropna(how='any', inplace=True, axis=0)
    elif strategy == MissingDataResolutionStrategy.DROP_FEATURE:
        df.dropna(how='any', inplace=True, axis=1)
    else:
        # Replace missing values with median for that column, only go through numeric features
        df_numeric = df.select_dtypes(include=[np.number])
        numeric_cols = df_numeric.columns.values

        for col in numeric_cols:
            missing = df[col].isnull()
            num_missing = np.sum(missing)

            if num_missing > 0:
                med = df[col].median()
                df[col] = df[col].fillna(med)

    log(df, "After handle missing data")

    return df


def handle_columns_with_outstanding_deviation(df):
    log(df, "Before handling of std deviation")

    df = df.drop(df.std()[df.std() < .3].index.values, axis=1)
    df = df.drop(df.std()[df.std() > 1000].index.values, axis=1)

    log(df, "After handling of std deviation")

    return df


def scale_numeric_data(df, has_label=True):
    log(df, "Scaling data")
    min_max_scaler = MinMaxScaler()

    if has_label: # Do not scale the label column
        df[df.columns[0: -1]] = MinMaxScaler().fit_transform(df.iloc[:, 0:-1])
        return df

    return min_max_scaler.fit_transform(df)


def remove_duplicate_observations(df):
    df_dedupped = df.drop_duplicates()
    log(df, "Before removing duplicates")
    log(df_dedupped, "After removing duplicates")


def log(df, step):
    print("---> Data status for step '{}' is: shape={}".format(step, df.shape))























