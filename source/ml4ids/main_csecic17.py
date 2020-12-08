from argparse import ArgumentParser
import pandas as pd

from ml_for_ids.datasets.datset_info import DATASET_ROOT_DIR, IDSDataset
from ml_for_ids.datasets.dataset_ingestion import load_csv_dataset
from ml_for_ids.datasets.dataset_preprocess import *
from ml_for_ids.datasets.dataset_preprocess import split_data, split_data_and_labels_cols
from ml_for_ids.ml_models.dnn import SimpleDNNModel

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure


matplotlib.rcParams['figure.figsize'] = (12,8)


SAMPLED_CSV_PATH = "dataset/unsw_nb15/predefined/UNSW_NB15_training-set.csv"


def parse_cmd_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-s", "--simple", action="store_true", help="Use predefined training and testing sets which are reduced in size for faster processing")
    arg_parser.add_argument("-ot", "--only-test", action="store_true", help="Skip training, load latest trained model and perform test")
    return arg_parser.parse_args()


def main():
    args = parse_cmd_args()
    dataset = IDSDataset.CSE_CIC_IDS_2017

    if args.simple:
        # Load smaller - sampled CSV
        df = pd.read_csv(SAMPLED_CSV_PATH, usecols=dataset.get_attrs())

        analyze_missing_data(df)
        df = handle_missing_data(df)
        df = handle_columns_with_outstanding_deviation(df)
        df = scale_numeric_data(df)
        df = remove_duplicate_observations(df)

        x_train, x_test, y_train, y_test = split_data(df, target_map_fun=IDSDataset.get_target_map_fun(dataset))
    else:
        # Load full data set (4 CSVs)
        data_frame = load_csv_dataset(dir_with_csvs=DATASET_ROOT_DIR + IDSDataset.UNSW_NB15.get_dataset_dir())
        data_frame = dataset_cleanup(data_frame)
        x_train, x_test, y_train, y_test = split_data(data_frame)

    model = SimpleDNNModel(x_train, x_test, y_train, y_test, dataset.get_dataset_dir())
    model.train()
    model.test()
    model.save()
    model.plot_confusion_matrix()


main()