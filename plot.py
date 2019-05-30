import datetime

import matplotlib.pyplot as plt
import os

import pandas as pd

from general import candidates_path_2012, candidates_path_2016, statements_path, get_fn, candidates_path

from pandas.plotting import register_matplotlib_converters


def plot_truthiness():
    register_matplotlib_converters()
    plot_truthiness_2012()
    plot_truthiness_2016()
    plot_truthiness_2020()


def plot_truthiness_2012():
    start = datetime.datetime.strptime('January 21 2009', '%B %d %Y')
    end = datetime.datetime.strptime('November 5 2012', '%B %d %Y')
    df = pd.read_csv(candidates_path_2012, header=0)

    # First, get the candidates who ran in 2012.
    plot_truthiness_generic(df, start, end, 'truthiness_2012.svg')


def plot_truthiness_2016():
    start = datetime.datetime.strptime('January 21 2012', '%B %d %Y')
    end = datetime.datetime.strptime('November 8 2016', '%B %d %Y')
    df = pd.read_csv(candidates_path_2016, header=0)

    # First, get the candidates who ran in 2012.
    plot_truthiness_generic(df, start, end, 'truthiness_2016.svg')


def plot_truthiness_2020():
    start = datetime.datetime.strptime('January 21 2016', '%B %d %Y')
    end = datetime.datetime.strptime('November 3 2020', '%B %d %Y')
    df = pd.read_csv(candidates_path, header=0)

    # First, get the candidates who ran in 2012.
    plot_truthiness_generic(df, start, end, 'truthiness_2020.svg')


def plot_truthiness_generic(df: pd.DataFrame, start: datetime.datetime, end: datetime.datetime, title: str):
    figsize = (35, 40)
    fname = os.path.join(os.path.join(os.getcwd(), 'images'), title)

    fig, ax = plt.subplots(len(df), 1, figsize=figsize, sharex=True, sharey=True)
    i = 0

    for n in list(df['Name']):
        fn = get_fn(n)
        print('fn: {}'.format(fn))
        filename = os.path.join(statements_path, fn + '.csv')

        df_mini = pd.read_csv(filename, header=0)
        df_mini['date'] = pd.to_datetime(df_mini['date'], format='%B %d %Y')
        df_mini = df_mini[df_mini['date'] >= start]
        df_mini = df_mini[df_mini['date'] <= end]
        df_mini = df_mini.reset_index(drop=True)

        if len(df_mini) == 0:
            continue

        # print(df_mini.head())

        ax[i].plot(df_mini['date'], df_mini['verdict'], label=n)
        ax[i].legend(loc=2)
        ax[i].set_xlabel('Date')
        ax[i].set_ylabel('Degree of falsehood')
        ax[i].set_xlim([start, end])
        ax[i].set_ylim([-1, 6])
        i += 1

    # Set a legend on the upper left.
    fig.suptitle('Truthiness')
    fig.savefig(fname)