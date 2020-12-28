import tensorflow as tf
from tensorflow import keras as k
import numpy as np

# https://ax.dev/ - Adaptive Experimentation Platform
from ax.service.ax_client import AxClient
from ax.utils.notebook.plotting import render, init_notebook_plotting


def build_dnn_model(x_train,
                    num_hidden_layers,
                    num_neurons_per_layer,
                    dropout_rate,
                    activation):

    inputs = k.Input(shape=(x_train.shape[1],))
    x = k.layers.Dropout(dropout_rate)(inputs)

    for i in range(num_hidden_layers):
        x = k.layers.Dense(num_neurons_per_layer, activation=activation)(x)
        x = k.layers.Dropout(dropout_rate)(x)

    outputs = k.layers.Dense(1, activation='linear')(x)

    model = k.Model(inputs=inputs, outputs=outputs)

    return model


# This function takes in the hyperparameters and returns a score (Cross validation).
def keras_mlp_cv_score(x_train, y_train, parameters, weight=None):
    model = build_dnn_model(x_train,
                            parameters.get('num_hidden_layers'),
                            parameters.get('neurons_per_layer'),
                            parameters.get('dropout_rate'),
                            parameters.get('activation'))

    opt = parameters.get('optimizer')
    opt = opt.lower()

    learning_rate = parameters.get('learning_rate')

    if opt == 'adam':
        optimizer = k.optimizers.Adam(lr=learning_rate)
    elif opt == 'rms':
        optimizer = k.optimizers.RMSprop(lr=learning_rate)
    else:
        optimizer = k.optimizers.SGD(lr=learning_rate)

    model.compile(optimizer=optimizer,
                  loss=k.losses.MeanSquaredError(),
                  metrics=['mse', 'accuracy'])

    data = x_train
    labels = y_train

    res = model.fit(data, labels, epochs=25, batch_size=parameters.get('batch_size'),
                    validation_split=0.2)

    # look at the last 10 epochs. Get the mean and standard deviation of the validation score.
    last10_scores = np.array(res.history['val_loss'][-10:])
    mean = last10_scores.mean()
    sem = last10_scores.std()

    # Nan means that model didn't converge
    if np.isnan(mean):
        return 9999.0, 0.0

    return mean, sem


# Search space
parameters = [
    {
        "name": "learning_rate",
        "type": "range",
        "bounds": [0.0001, 0.5],
        "log_scale": True,
    },
    {
        "name": "dropout_rate",
        "type": "range",
        "bounds": [0.01, 0.5],
        "log_scale": True,
    },
    {
        "name": "num_hidden_layers",
        "type": "range",
        "bounds": [1, 5],
        "value_type": "int"
    },
    {
        "name": "neurons_per_layer",
        "type": "range",
        "bounds": [1, 250],
        "value_type": "int"
    },
    {
        "name": "batch_size",
        "type": "choice",
        "values": [8, 16, 32, 64, 128, 256],
    },

    {
        "name": "activation",
        "type": "choice",
        "values": ['tanh', 'sigmoid', 'relu'],
    },
    {
        "name": "optimizer",
        "type": "choice",
        "values": ['adam', 'rms', 'sgd'],
    },
]


def run_hyperparameter_optimization(x_train, y_train, params=parameters):
    init_notebook_plotting()

    ax_client = AxClient()
    ax_client.create_experiment(
        name="keras_dnn_experiment",
        parameters=params,
        objective_name='keras_cv',
        minimize=True)

    def evaluate(params):
        return {"keras_cv": keras_mlp_cv_score(x_train, y_train, params)}

    for i in range(100):
        params, trial_index = ax_client.get_next_trial()
        ax_client.complete_trial(trial_index=trial_index, raw_data=evaluate(params))
