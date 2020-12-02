from keras.layers import Dense
from keras.models import Sequential
from keras.models import model_from_json
from keras.callbacks import EarlyStopping
from keras.callbacks import CSVLogger
from sklearn.metrics import confusion_matrix

from ml_for_ids.ml_models.base.binary_classifier import BinaryClassifier
from ml_for_ids.utils import *


class SimpleDNNModel(BinaryClassifier):
    def __init__(self, x_train=None, x_test=None, y_train=None, y_test=None, dataset_dir_name=None):
        super().__init__(x_train, x_test, y_train, y_test, dataset_dir_name)
        self.model = Sequential()
        if x_train is not None:
            self.__setup_layers(len(x_train[0]))
        self.model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
        self._training_history = None
        self._test_loss = None
        self._test_accuracy = None
        self._confusion_matrix = None

    def __setup_layers(self, input_size):
        self.model.add(Dense(256, activation='relu', input_dim=input_size))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))

    def train(self, x_train=None, y_train=None, training_setup=None):
        if x_train is None:
            x_train = self.x_train
        if y_train is None:
            y_train = self.y_train
        if training_setup is None:
            training_setup = dict(n_epochs=20, batch_size=20)

        csv_logger = CSVLogger(self.trained_model_dir + "/" + get_time_based_file_name("log"))
        early_stopping = EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=10, restore_best_weights=True)
        self._training_history = self.model.fit(x_train, y_train, epochs=training_setup["n_epochs"],
                                                batch_size=training_setup["batch_size"], shuffle=True, verbose=1,
                                                callbacks=[csv_logger, early_stopping])

    def test(self, x_test=None, y_test=None):
        if x_test is None:
            x_test = self.x_test
        if y_test is None:
            y_test = self.y_test

        self._test_loss, self._test_accuracy = self.model.evaluate(x_test, y_test, verbose=1)
        print('Test loss:', self._test_loss)
        print('Test accuracy:', self._test_accuracy)

    def save(self):
        saved_json_file_path = save_json_to_file(self.trained_model_dir, self.model.to_json())
        self.model.save_weights(saved_json_file_path.replace("json", "h5"))

    def load(self):
        try:
            latest_json_file_name, json_content = load_last_file(self.trained_model_dir)
            self.model = model_from_json(json_content)
            self.model.load_weights(latest_json_file_name.replace("json", "h5"))
            # self.model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
        except Exception as e:
            raise Exception("Failed to load model\n{}".format(e))

    def ml_method_name(self):
        return "dnn"

    def plot_confusion_matrix(self):
        y_pred = self.model.predict(self.x_test)

        y_pred[y_pred > 0.5] = 1
        y_pred[y_pred <= 0.5] = 0

        self._confusion_matrix = confusion_matrix(self.y_test, y_pred)
        print(self._confusion_matrix)

    def predict(self, x):
        return self.model.predict(x, verbose=0)

