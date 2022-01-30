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
    xmin=0,
    xmax=13,
):
    plt.figure(facecolor=(0.99, 0.97, 0.97), dpi=300)
    ax = plt.axes()
    ax.set_facecolor((0.99, 0.97, 0.97))
    plt.fill_between(xx, df.SD0.values, df.SD1.values, color="green", alpha=0.4)
    plt.fill_between(xx, df.SD1.values, df.SD2.values, color="yellow", alpha=0.4)
    plt.fill_between(xx, df.SD2.values, df.SD3.values, color="red", alpha=0.4)
    plt.plot(xx, df.SD0.values, color="black", label="WHO average")
    plt.fill_between(xx, df.SD1neg.values, df.SD0.values, color="green", alpha=0.4)
    plt.fill_between(xx, df.SD2neg.values, df.SD1neg.values, color="yellow", alpha=0.4)
    plt.fill_between(xx, df.SD3neg.values, df.SD2neg.values, color="red", alpha=0.4)
    plt.scatter(x_J, y_J, label="Jennifer")
    plt.xlim(xmin=xmin, xmax=xmax)
    plt.ylim(ymin=y_min, ymax=y_max)
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

    df2 = pd.DataFrame(data)
    df2["date"] = pd.to_datetime(df2["date"], dayfirst=True).dt.date
    df2[["week", "weight"]] = df2[["week", "weight"]].astype(float)
    x_J = df2["week"].values
    y_J = df2["weight"].values

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
        "Weight [kg]",
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

    df2 = pd.DataFrame(data)
    df2 = df2.astype(float)
    x_J = df2["week"].values
    y_J = df2["height"].values

    plot_fcn(
        xx,
        df,
        x_J,
        y_J,
        40,
        67,
        ARTIFACT_PATH,
        "height.jpg",
        "Weeks",
        "Height [cm]",
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

    df2 = pd.DataFrame(data)
    df2 = df2.astype(float)
    x_J = df2["week"].values
    y_J = df2["head"].values

    plot_fcn(
        xx,
        df,
        x_J,
        y_J,
        30,
        44,
        ARTIFACT_PATH,
        "head.jpg",
        "Weeks",
        "Head Circumference [cm]",
        "Head Circumference by Weeks",
    )
    return


def plot_wh(weight_data, height_data):
    PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
    SOURCE_DATA_FILE = PROJECT_PATH / "data/wfl_girls_0-to-2-years_zscores.csv"
    ARTIFACT_PATH = PROJECT_PATH / "static"

    df = pd.read_csv(SOURCE_DATA_FILE)
    del_cols = ["L", "M", "S"]
    df = df.drop(columns=del_cols)
    xx = df.Length.values

    df_height = pd.DataFrame(height_data)
    df_height = df_height.astype(float)

    df_weight = pd.DataFrame(weight_data)
    df_weight["date"] = pd.to_datetime(df_weight["date"], dayfirst=True).dt.date
    df_weight[["week", "weight"]] = df_weight[["week", "weight"]].astype(float)

    x_J = df_height["height"].values
    y_J = df_weight["weight"].values

    plot_fcn(
        xx,
        df,
        x_J,
        y_J,
        0,
        10,
        ARTIFACT_PATH,
        "wh.jpg",
        "Height [cm]",
        "Weight [kg]",
        "Weight/Height",
        xmin=48,
        xmax=65,
    )
    return


def plot_feeding(feeding_data, weight_data):
    PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
    ARTIFACT_PATH = PROJECT_PATH / "static"
    
    df = pd.DataFrame(feeding_data)
    df2 = df[["date", "total_vol"]].copy()
    df2["total_vol"] = df2.total_vol.astype(int)
    df2["date"] = pd.to_datetime(df2["date"], dayfirst=True).dt.date
    df2["J_ma3"] = df2['total_vol'].rolling(7).mean()

    df_weight = pd.DataFrame(weight_data)
    df_weight["date"] = pd.to_datetime(df_weight["date"], dayfirst=True).dt.date
    df_weight[["week", "weight"]] = df_weight[["week", "weight"]].astype(float)
    df_weight["total_feed"] = 150 * df_weight.weight
    df_weight["total_feed_low"] = 130 * df_weight.weight
    df_weight["total_feed_high"] = 170 * df_weight.weight

    # Plot eating
    plt.figure(facecolor=(0.99, 0.97, 0.97), dpi=300)
    ax = plt.axes()
    ax.set_facecolor((0.99, 0.97, 0.97))
    plt.bar(df2.date, df2.total_vol.values, label='Daily Volume Eaten')
    plt.plot(df2.date, df2.J_ma3,color="red", alpha=0.6, label="Jen 7-day MA")
    plt.plot(df_weight.date, df_weight.total_feed, color="orange", label="Calc Requirement")
    plt.fill_between(
        df_weight.date,
        df_weight.total_feed_high,
        df_weight.total_feed_low,
        color="green",
        alpha=0.4,
    )
    plt.margins(0.01,0.1)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Volume Food per Day [ml]")
    plt.legend()
    plt.title("Daily Food Intake")
    plt.savefig(ARTIFACT_PATH / "feeding.jpg", bbox_inches='tight')

    return 


def plot_prop(feeding_data):
    PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
    ARTIFACT_PATH = PROJECT_PATH / "static"

    df = pd.DataFrame(feeding_data)
    df["bm_vol"] = df.bm_vol.astype(int)
    df["formula_vol"] = df.formula_vol.astype(int)

    df["date"] = pd.to_datetime(df["date"], dayfirst=True).dt.date
    df["total_vol"] = df.bm_vol + df.formula_vol
    df["bm_prop"] = df.bm_vol / df.total_vol
    df["form_prop"] = df.formula_vol / df.total_vol

    # Plot eating
    plt.figure(dpi=300)
    plt.bar(df.date, df.bm_prop.values, label="Formula")
    plt.bar(df.date, df.form_prop.values, bottom=df.bm_prop.values, label="BM")

    plt.xticks(rotation=45, ha="right")
    plt.savefig(ARTIFACT_PATH / "proportion.jpg")

    return
