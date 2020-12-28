import os

from argparse import ArgumentParser

import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2, f_classif, mutual_info_classif

from sklearn.utils import shuffle

from ml_for_ids.utils import *
from ml_for_ids.datasets.datset_info import *
from ml_for_ids.datasets.dataset_ingestion import *
from ml_for_ids.datasets.dataset_preprocess import *
from ml_for_ids.datasets.dataset_visualization import *
from ml_for_ids.ml_models.dnn import SimpleDNNModel
from ml_for_ids.datasets.hyper_parameter_optimization import run_hyperparameter_optimization


SAMPLED_CSV_PATH = "dataset/csecic2018/predefined/sample_data.csv"

OUTPUT_DIR = "reports/" + get_time_based_dir_name()
os.mkdir(OUTPUT_DIR)
os.mkdir(OUTPUT_DIR + "/images")

EXCLUDED_FEATURES = [
    CICIDS18Feature.DST_PORT.get_raw_col_name(),
    CICIDS18Feature.TIMESTAMP.get_raw_col_name(),
    CICIDS18Feature.PROTOCOL.get_raw_col_name()
]


def parse_cmd_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-s", "--simple", action="store_true", help="Use predefined training and testing sets which are reduced in size for faster processing")
    arg_parser.add_argument("-ot", "--only-test", action="store_true", help="Skip training, load latest trained model and perform test")
    arg_parser.add_argument("-r", "--remote", action="store_true", help="Indicates that the script is run on a remote server (Colab)")
    arg_parser.add_argument("-v", "--with-visualization", action="store_true", help="Indicates that the plotting should be done")
    return arg_parser.parse_args()


def main():
    print("Current working directory:{}".format(os.getcwd()))

    args = parse_cmd_args()
    dataset = IDSDataset.CSE_CIC_IDS_2018

    if args.simple:
        df = pd.read_csv(dataset.get_sample_csv_path())
    else:
        df = load_csv_dataset(dir_with_csvs=DATASET_ROOT_DIR + dataset.get_dataset_dir())

    for col in dataset.get_cols_to_ignore():
        del df[col]

    df = remove_duplicate_observations(df)

    desc = describe_dataset(df)
    save_desc(desc)

    df = shuffle(df)

    df = cast_to_float(df)

    analyze_missing_data(df)

    df = handle_negative_and_inf_values(df)
    df = handle_missing_data(df)

    if args.with_visualization:
        plot_histogram_for_each_feature(df, destination_path_supplier=get_image_path("hist"))
        plot_boxplot_for_each_feature(df, destination_path_supplier=get_image_path("box"))

    handle_outliers(df)

    df = scale_numeric_data(df)  #, scaler=RobustScaler(with_centering=False))
    df = remove_duplicate_observations(df)

    if args.with_visualization:
        plot_histogram_for_each_feature(df, destination_path_supplier=get_image_path("hist"))
        plot_boxplot_for_each_feature(df, destination_path_supplier=get_image_path("box"))

    x_train, x_test, y_train, y_test = split_data(df, target_map_fun=IDSDataset.get_target_map_fun(dataset))

    model = SimpleDNNModel(x_train, x_test, y_train, y_test, dataset.get_dataset_dir())
    model.train()
    model.test()
    model.save()
    model.plot_confusion_matrix()

    run_hyperparameter_optimization(x_train, y_train)


def describe_dataset(df):
    desc = df.describe()
    print("DATASET DESC")
    print(desc)
    return desc


def get_image_path(plot_type):
    return lambda x: OUTPUT_DIR + "/images/{}_{}_{}".format(x.replace("/", "_"), plot_type, get_time_based_file_name("png"))


def save_desc(desc):
    pd.DataFrame(desc).to_csv(OUTPUT_DIR + "/dataset_meta.csv")


main()
