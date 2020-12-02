from argparse import ArgumentParser
from enum import IntEnum

from ml_for_ids.datasets.datset_info import DATASET_ROOT_DIR, IDSDataset
from ml_for_ids.datasets.dataset_ingestion import load_csv_dataset
from ml_for_ids.datasets.dataset_preprocess import dataset_cleanup
from ml_for_ids.datasets.dataset_preprocess import split_data
from ml_for_ids.ml_models.dnn import SimpleDNNModel
from ml_for_ids.training_setup import setups


class MLMethod(IntEnum):
    DNN = 1


class DatasetAction(IntEnum):
    TRAIN = 1
    TEST = 2


def parse_cmd_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-ds", "--dataset", type=int, help="Dataset number (0 - UNSW_NB15, 1 - CIC_IDS_2017, 2 - CIC_IDS_2018" )
    arg_parser.add_argument("-so", "--save-output", action="store_true", help="Save training output")
    arg_parser.add_argument("-od", "--output-dir", help="Directory for saving output")
    arg_parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    arg_parser.add_argument("-st", "--skip-training", action="store_true", help="Skip model training and load pretrained model")
    arg_parser.add_argument("-us", "--use-setup", action="store_true", help="Use predefined setup for multiple traning sessions")
    return arg_parser.parse_args()


def main():
    if __name__ == "__main__":
        args = parse_cmd_args()

        if args.interactive:
            interactive_mode()
        elif args.dataset:
            process(datasets=[IDSDataset(args.dataset)],
                    setups=setups if args.use_setup else None,
                    actions=[DatasetAction.TRAIN if not args.skip_training else None, DatasetAction.TEST])
        elif args.skip_training:
            process(actions=[DatasetAction.TEST])
        else:
            process()


def interactive_mode():
    while True:
        print("Select dataset:")
        for k, v in enumerate(IDSDataset):
            print("{}-{}".format(k + 1, v.name))
        selected_dataset = int(input())

        if selected_dataset not in list(map(int, IDSDataset)):
            raise Exception("Invalid dataset selected")

        for k, v in enumerate(MLMethod):
            print("{}-{}".format(k + 1, v.name))
        selected_ml_method = int(input())

        if int(selected_ml_method) not in list(map(int, MLMethod)):
            raise Exception("Invalid ML method selected")

        for k, v in enumerate(DatasetAction):
            print("{}-{}".format(k + 1, v.name))
        selected_action = int(input())

        if int(selected_action) not in list(map(int, DatasetAction)):
            raise Exception("Invalid action selected")

        process([IDSDataset(selected_dataset)], [MLMethod(selected_ml_method)], [DatasetAction(selected_action)])

        print("Continue? (y/n)")
        if input() != "y":
            break


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


def process(datasets=[IDSDataset.UNSW_NB15, IDSDataset.CSE_CIC_IDS_2017, IDSDataset.UNSW_NB15],
            ml_methods=[MLMethod.DNN],
            actions=[DatasetAction.TRAIN, DatasetAction.TEST],
            setups=[dict(n_epochs=20, batch_size=20)]):
    for dataset in datasets:
        data_frame = load_csv_dataset(dir_with_csvs=DATASET_ROOT_DIR + dataset.get_dataset_dir(),
                                      use_columns=dataset.get_attrs())
        data_frame = dataset_cleanup(data_frame)

        # Split data from pandas DataFrame to Numpy arrays for training and testing
        x_train, x_test, y_train, y_test = split_data(data_frame, target_map_fun=IDSDataset.get_target_map_fun(dataset))

        for ml_method in ml_methods:
            if ml_method == MLMethod.DNN:
                _process(SimpleDNNModel(x_train, x_test, y_train, y_test, dataset.get_dataset_dir()), actions, setups)


main()
