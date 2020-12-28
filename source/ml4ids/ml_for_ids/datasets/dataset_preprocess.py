from enum import IntEnum

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.utils import shuffle

from ml_for_ids.datasets.dataset_visualization import *


class MissingDataResolutionStrategy(IntEnum):
    DROP_OBSERVATION = 1,
    DROP_FEATURE = 2,
    REPLACE_WITH_MEAN = 3


# Feature extraction - later on
# test = SelectKBest(score_func=chi2, k=10)
def split_data(df, target_map_fun=None):
    X, Y = split_data_and_labels_cols(df, target_map_fun)
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

    return X, Y


def cast_to_float(df):
    log(df, "Before handle non numeric cols")
    print("### Column types before casting: {}".format(df.dtypes))
    df.iloc[:, 0:-1] = df.iloc[:, 0:-1].astype(dtype=float)
    print("### Column types after casting: {}".format(df.dtypes))
    log(df, "After handle non numeric cols")
    return df


def analyze_missing_data(df):
    log_missing_data_info(df)
    plot_missing_data_info(df)


def log_missing_data_info(df):
    for col in df.columns:
        pct_missing = np.mean(df[col].isnull())
        print('{} - {}%'.format(col, round(pct_missing * 100)))


def handle_negative_and_inf_values(df):
    df = df.replace([np.inf, -np.inf], np.nan)

    for col in df.columns:
        if df[col].dtype == float or df[col].dtype == int:
            vals = df[col]
            num_neg = len(vals[vals < 0])
            num_inf = len(vals[vals == np.inf])
            num_inf += len(vals[vals == -np.inf])

            if num_neg > 0:
                print("Col {} contains {} negative values".format(col, num_neg))
                mean = vals[vals > 0].mean()
                df[col][df[col] < 0] = mean

            if num_inf > 0:
                print("Col {} contains {} infinite values".format(col, num_inf))
                mean = vals[vals > 0].mean()
                df[col][df[col] == np.inf | df[col] == -np.inf] = mean

    return df


def handle_outliers(df):
    log(df, "Handle outliers")
    cols_to_remove = []

    for col in df.columns:
        if (df[col].dtype == float or df[col].dtype == int) and col.lower() != "label":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            _90th = df[col].quantile(0.9)
            _95th = df[col].quantile(0.95)
            _98th = df[col].quantile(0.98)
            IQR = Q3 - Q1
            max_val = df[col].max()

            log_quantiles(col, Q1, Q3, IQR, _90th, _95th, _98th, max_val, df[col].skew())

            if Q1 == 0 and Q3 == 0:
                print("Removing column because at least 75% are zeros")
                cols_to_remove.append(col)
            else:
                # We handle outliers by cutting them to the value of 95th percentile
                df[col] = np.where(df[col] > _95th, _95th, df[col])
                print("Skew value after ={}".format(df[col].skew()))

    for col in cols_to_remove:
        del df[col]


def exec_z_score_eval(df):
    from scipy import stats
    z = np.abs(stats.zscore(df.hp))
    print(z)


def handle_missing_data(df, strategy=MissingDataResolutionStrategy.DROP_OBSERVATION):
    log(df, "Before handle missing data")

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

    for col in df.columns:
        print("Std dev for col={}, std={}".format(col, df[col].std))

    df = df.drop(df.std()[df.std() < .1].index.values, axis=1)
    df = df.drop(df.std()[df.std() > 1000].index.values, axis=1)

    log(df, "After handling of std deviation")

    return df


def scale_numeric_data(df, scaler=None, has_label=True):
    log(df, "Scaling data")

    if scaler is None:
        scaler = MinMaxScaler()

    if has_label:  # Do not scale the label column
        df.loc[:, df.columns[0: -1]] = scaler.fit_transform(df.iloc[:, 0:-1])
        return df

    return scaler.fit_transform(df)


def remove_duplicate_observations(df):
    df_dedupped = df.drop_duplicates()
    log(df, "Before removing duplicates")
    log(df_dedupped, "After removing duplicates")
    return df_dedupped


def log(df, step):
    print("---> Data status for step '{}' is: shape={}".format(step, df.shape))
    print("---> Cols: {}".format(df.columns))


def log_quantiles(col, q1, q3, iqr, _90th, _95th, _98th, max, skew):
    print("Column '{}'\n==> q1={}, q3={}, IRQ={}\n==>90th={}, 95th={}, 98th={}\nmax={}\nskew={}"
          .format(col, q1, q3, iqr, _90th, _95th, _98th, max, skew))





















