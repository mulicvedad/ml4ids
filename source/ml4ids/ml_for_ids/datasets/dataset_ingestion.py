import os
import glob
import pandas as pd


def load_csv_dataset(dir_with_csvs, num_rows=None, use_columns=None):
    if not os.path.exists(dir_with_csvs):
        raise Exception("Dir with csvs not exists")

    li = []
    csv_paths = glob.glob(os.path.join(dir_with_csvs, "*"))

    for path in csv_paths:
        df = pd.read_csv(path, index_col=None, header=0, nrows=num_rows, usecols=use_columns)
        li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)