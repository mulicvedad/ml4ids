import numpy as np

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure

matplotlib.rcParams['figure.figsize'] = (12, 8)

from ml_for_ids.utils import  get_time_based_file_name


def plot_confusion_matrix(cm, save_to=None):
    pass


def plot_missing_data_info(df):
    plot_missing_data_heatmap(df)
    plot_missing_data_histogram(df)


def plot_missing_data_heatmap(df):
    import seaborn as sns
    colours = ['#E27B65', '#50A372']  # Mark rows with missing data with red color, otherwise green
    sns.heatmap(df.isnull(), cmap=sns.color_palette(colours))
    plt.show()


def plot_missing_data_histogram(df):
    df_for_plot = df.copy()
    for col in df_for_plot.columns:
        missing = df_for_plot[col].isnull()
        num_missing = np.sum(missing)

        if num_missing > 0:
            print('created missing indicator for: {}'.format(col))
            df_for_plot['{}_ismissing'.format(col)] = missing

    # then based on the indicator, plot the histogram of missing values
    ismissing_cols = [col for col in df_for_plot.columns if 'ismissing' in col]
    df_for_plot['num_missing'] = df_for_plot[ismissing_cols].sum(axis=1)
    df_for_plot['num_missing'].value_counts().reset_index().sort_values(by='index').plot.bar(x='index', y='num_missing')
    plt.show()


def plot_aggregate_histogram_for_features(df, num_features=None):
    if num_features is None:
        df.hist()
        plt.show()
    else:
        start = 0
        end = num_features
        num_all_features = len(df.columns)

        while end < num_all_features:
            selected_df = df.iloc[:, start:end]
            selected_df.hist(bins=30)
            plt.show()
            start += num_features
            end += num_features

        if end >= num_all_features:
            df.iloc[:, start:num_all_features].hist(bins=30)
            plt.show()


def plot_histogram_for_each_feature(df, destination_path_supplier=None):
    for col in df.columns:
        if df[col].dtype == float or df[col].dtype == int:
            plt.hist(df[col].values, bins=100, label=col)
            plt.show()
            if destination_path_supplier is not None:
                save_figure_from_plot(destination_path_supplier(col))


def plot_boxplot_for_each_feature(df, destination_path_supplier=None):
    for col in df.columns:
        if df[col].dtype == float or df[col].dtype == int:
            plt.boxplot(df[col], labels=[col])
            plt.show()
            if destination_path_supplier is not None:
                save_figure_from_plot(destination_path_supplier(col))


def save_figure_from_plot(path):
    fig = plt.gcf()
    fig.savefig(path, bbox_inches="tight")