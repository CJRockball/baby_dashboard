import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def plot_fcn(
    xx,
    df,
    x_J,
    y_J,
    y_min,
    y_max,
    ARTIFACT_PATH,
    fname,
    xlabel_name,
    ylabel_name,
    title_name,
):
    plt.figure()
    plt.fill_between(xx, df.SD0.values, df.SD1.values, color="green", alpha=0.4)
    plt.fill_between(xx, df.SD1.values, df.SD2.values, color="yellow", alpha=0.4)
    plt.fill_between(xx, df.SD2.values, df.SD3.values, color="red", alpha=0.4)
    plt.plot(xx, df.SD0.values, color="black", label="WHO average")
    plt.fill_between(xx, df.SD1neg.values, df.SD0.values, color="green", alpha=0.4)
    plt.fill_between(xx, df.SD2neg.values, df.SD1neg.values, color="yellow", alpha=0.4)
    plt.fill_between(xx, df.SD3neg.values, df.SD2neg.values, color="red", alpha=0.4)
    plt.scatter(x_J, y_J)
    plt.xlim(xmin=0, xmax=13)
    # plt.ylim(ymin=y_min, ymax=y_max)
    plt.grid()
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    plt.title(title_name)
    plt.legend()
    plt.savefig(ARTIFACT_PATH / fname)

    return


def plot_weight(data):
    PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
    SOURCE_DATA_FILE = PROJECT_PATH / "data/wfa_girls_0-to-13-weeks_zscores.csv"
    ARTIFACT_PATH = PROJECT_PATH / "static"

    df = pd.read_csv(SOURCE_DATA_FILE)
    del_cols = ["L", "M", "S"]
    df = df.drop(columns=del_cols)
    xx = df.Week.values

    x_J = data["week"].values()
    y_J = data["weight"].values()

    plot_fcn(
        xx,
        df,
        x_J,
        y_J,
        0,
        9,
        ARTIFACT_PATH,
        "weight.jpg",
        "Weeks",
        "Weight",
        "Weight by Weeks",
    )
    return


def plot_height(data):
    PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
    SOURCE_DATA_FILE = PROJECT_PATH / "data/lhfa_girls_0-to-13-weeks_zscores.csv"
    ARTIFACT_PATH = PROJECT_PATH / "static"

    df = pd.read_csv(SOURCE_DATA_FILE)
    del_cols = ["L", "M", "S"]
    df = df.drop(columns=del_cols)
    xx = df.Week.values

    x_J = data["week"].values()
    y_J = data["height"].values()

    plot_fcn(
        xx,
        df,
        x_J,
        y_J,
        40,
        69,
        ARTIFACT_PATH,
        "height.jpg",
        "Weeks",
        "Height",
        "Height by Weeks",
    )
    return


def plot_head(data):
    PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
    SOURCE_DATA_FILE = PROJECT_PATH / "data/hcfa-girls-0-13-zscores.csv"
    ARTIFACT_PATH = PROJECT_PATH / "static"

    df = pd.read_csv(SOURCE_DATA_FILE)
    del_cols = ["L", "M", "S"]
    df = df.drop(columns=del_cols)
    xx = df.Week.values

    x_J = data["week"].values()
    y_J = data["head"].values()

    plot_fcn(
        xx,
        df,
        x_J,
        y_J,
        0,
        9,
        ARTIFACT_PATH,
        "head.jpg",
        "Weeks",
        "Head Circumference",
        "Height Circumference by Weeks",
    )
    return
