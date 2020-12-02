import os


class BinaryClassifier:
    def __init__(self, x_train=None, x_test=None, y_train=None, y_test=None, dataset_dir=None):
        self.model = None
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.trained_model_dir = os.path.join("trained_models", dataset_dir, self.ml_method_name())

    def train(self, x_train, y_train, tranining_setup):
        pass

    def test(self, x_test, y_test):
        pass

    def plot_confusion_matrix(self):
        pass

    def load(self):
        pass

    def ml_method_name(self):
        return ""
