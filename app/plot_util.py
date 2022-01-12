import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


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
    plt.ylim(ymin=0, ymax=9)
    plt.grid()
    plt.xlabel("Weeks")
    plt.ylabel("Weight")
    plt.title("Weight by Weeks")
    plt.legend()
    plt.savefig(ARTIFACT_PATH / "weight.jpg")

    return
