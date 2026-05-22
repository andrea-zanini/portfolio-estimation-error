import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
cartella_plot = BASE_DIR / "results" / "plots"

def strategycomparison(returns_gmv: dict, returns_rp: dict, returns_eq: dict, method, window, frequency: list):
    for freq in frequency:
        gmv: pd.DataFrame = returns_gmv[method][window][freq]
        rp: pd.DataFrame = returns_rp[method][window][freq]
        eq: pd.DataFrame = returns_eq[window][freq]
        ret_gmv = gmv.squeeze().cumsum()
        ret_rp = rp.squeeze().cumsum()
        ret_eq = eq.squeeze().cumsum()
        plt.figure(figsize = (12, 6))
        sns.set_theme(
        style = "ticks",
        palette = "muted",
        font = "serif",
        rc={
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.4
            })
        sns.despine()
        sns.lineplot(x = ret_gmv.index, y = ret_gmv, label = "GMV")
        sns.lineplot(x = ret_rp.index, y = ret_rp, label = "RP")
        sns.lineplot(x = ret_eq.index, y = ret_eq, label = "EQ")
        plt.xlabel("Time")
        plt.ylabel("Return")
        plt.title("Strategy Comparison")
        plt.legend()
        plt.savefig(cartella_plot / f"Strategy_Comparison{method}{window}{freq}.png")
        plt.close()

def windoweffect(returns: dict, method, window: list, frequency):
    ret1: pd.DataFrame = returns[method][window[0]][frequency]
    ret2: pd.DataFrame = returns[method][window[1]][frequency]
    ret3: pd.DataFrame = returns[method][window[2]][frequency]
    ret_1 = ret1.squeeze().cumsum()
    ret_2 = ret2.squeeze().cumsum()
    ret_3 = ret3.squeeze().cumsum()
    plt.figure(figsize = (12, 6))
    sns.set_theme(
    style = "ticks",
    palette = "muted",
    font = "serif",
    rc={
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.4
        })
    sns.despine()
    sns.lineplot(x = ret_1.index, y = ret_1, label = f"{window[0]}")
    sns.lineplot(x = ret_2.index, y = ret_2, label = f"{window[1]}")
    sns.lineplot(x = ret_3.index, y = ret_3, label = f"{window[2]}")
    plt.xlabel("Time")
    plt.ylabel("Return")
    plt.title("Window Effect")
    plt.legend()
    plt.savefig(cartella_plot / f"Window_Effect.png")
    plt.close()

def shrinkageeffect(returns: dict, method: list, window, frequency):
    ret1: pd.DataFrame = returns[method[0]][window][frequency]
    ret2: pd.DataFrame = returns[method[1]][window][frequency]
    ret_1 = ret1.squeeze().cumsum()
    ret_2 = ret2.squeeze().cumsum()
    plt.figure(figsize = (12, 6))
    sns.set_theme(
    style = "ticks",
    palette = "muted",
    font = "serif",
    rc={
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.4
        })
    sns.despine()
    sns.lineplot(x = ret_1.index, y = ret_1, label = f"{method[0]}")
    sns.lineplot(x = ret_2.index, y = ret_2, label = f"{method[1]}")
    plt.xlabel("Time")
    plt.ylabel("Return")
    plt.title("Shrink Effect")
    plt.legend()
    plt.savefig(cartella_plot / f"Shrinkage_Effect.png")
    plt.close()

def drawdownplot(returns_gmv: pd.DataFrame, returns_rp: pd.DataFrame, returns_eq: pd.DataFrame):
    gmv = np.exp(returns_gmv.squeeze().cumsum())
    rp = np.exp(returns_rp.squeeze().cumsum())
    eq = np.exp(returns_eq.squeeze().cumsum())
    drawdown_gmv = (gmv - gmv.cummax()) / gmv.cummax()
    drawdown_rp = (rp - rp.cummax()) / rp.cummax()
    drawdown_eq = (eq - eq.cummax()) / eq.cummax()
    plt.figure(figsize = (12, 6))
    sns.set_theme(
    style = "ticks",
    palette = "muted",
    font = "serif",
    rc={
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.4
        })
    sns.despine()
    sns.lineplot(x = drawdown_gmv.index, y = drawdown_gmv, label = "GMV")
    sns.lineplot(x = drawdown_rp.index, y = drawdown_rp, label = "RP")
    sns.lineplot(x = drawdown_eq.index, y = drawdown_eq, label = "EQ")
    plt.xlabel("Time")
    plt.ylabel("Return")
    plt.title("Drawdown Comparison")
    plt.legend()
    plt.savefig(cartella_plot / f"Drawdown.png")
    plt.close()