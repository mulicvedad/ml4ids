from argparse import ArgumentParser
from enum import IntEnum
import pandas as pd

from ml_for_ids.datasets.datset_info import DATASET_ROOT_DIR, IDSDataset
from ml_for_ids.datasets.dataset_ingestion import load_csv_dataset
from ml_for_ids.datasets.dataset_preprocess import dataset_cleanup
from ml_for_ids.datasets.dataset_preprocess import split_data, split_data_and_labels_cols
from ml_for_ids.ml_models.dnn import SimpleDNNModel

PREDEFINED_TRAINING_CSV_PATH = "dataset/unsw_nb15/predefined/UNSW_NB15_training-set.csv"
PREDEFINED_TESTING_CSV_PATH = "dataset/unsw_nb15/predefined/UNSW_NB15_testing-set.csv"

class MLMethod(IntEnum):
    DNN = 1


class DatasetAction(IntEnum):
    TRAIN = 1
    TEST = 2


def parse_cmd_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-s", "--simple", action="store_true", help="Use predefined training and testing sets which are reduced in size for faster processing")
    arg_parser.add_argument("-ot", "--only-test", action="store_true", help="Skip training, load latest trained model and perform test")
    return arg_parser.parse_args()


def _process(binary_classifier, actions, setups):
    for setup in setups:
        if DatasetAction.TRAIN in actions:
            binary_classifier.train(training_setup=setup)
            binary_classifier.save()
        else:
            binary_classifier.load()

        binary_classifier.test()
        binary_classifier.plot_confusion_matrix()

        if DatasetAction.TRAIN not in actions:
            break


def main():
    args = parse_cmd_args()

    if args.simple:
        train_df = pd.read_csv(PREDEFINED_TRAINING_CSV_PATH, usecols=IDSDataset.UNSW_NB15.get_attrs())
        test_df = pd.read_csv(PREDEFINED_TESTING_CSV_PATH, usecols=IDSDataset.UNSW_NB15.get_attrs())
        data = pd.concat([train_df, test_df])
        data = dataset_cleanup(data)

        train_df = data[0:train_df.shape[0]]
        x_train, y_train = split_data_and_labels_cols(train_df)

        test_df = data[train_df.shape[0]:]
        x_test, y_test = split_data_and_labels_cols(test_df)
    else:
        # Load full data set (4 CSVs)
        data_frame = load_csv_dataset(dir_with_csvs=DATASET_ROOT_DIR + IDSDataset.UNSW_NB15.get_dataset_dir())
        data_frame = dataset_cleanup(data_frame)
        x_train, x_test, y_train, y_test = split_data(data_frame)

    model = SimpleDNNModel(x_train, x_test, y_train, y_test, IDSDataset.UNSW_NB15.get_dataset_dir())
    model.train()
    model.test()
    model.save()
    model.plot_confusion_matrix()


main()
