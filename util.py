import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import constants


def load_data(path):
    df = pd.read_csv(path)
    df[constants.DATE_COLUMN] = pd.to_datetime(df[constants.DATE_COLUMN], format=constants.DATE_FORMAT)

    return df


def create_subplots():
    return plt.subplots(nrows=2, ncols=5, constrained_layout=True)


def new_subplot():
    return plt.figure().add_subplot()


def plot_data(
    axis,
    x_values,
    y_values,
    title,
    y_label=None
):
    axis.set_title(title)
    axis.grid()
    if y_label is not None:
        axis.set_ylabel(y_label)
    axis.plot(x_values, y_values)


def show_correlation(returns):
    corr = np.corrcoef(np.array(returns))
    corr_df = pd.DataFrame(corr, index=constants.titles, columns=constants.titles)
    mask = np.triu(np.ones_like(corr_df, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    new_subplot()
    sns.heatmap(corr_df, mask=mask, cmap=cmap, square=True, linewidths=.5)
