import numpy as np
import pandas as pd

def stats(net_returns: pd.DataFrame, turnover: pd.DataFrame, method: list, window: list, rebalance_frequency: list, kind: str, rf):
    rows = []
    if kind == "EQ":
        for days in window:
            for freq in rebalance_frequency:
                ann_factor = {
                    "D": 252,
                    "W": 52,
                    "M": 12
                }[freq]
                ret = net_returns[days][freq].squeeze()
                cum_returns = ret.cumsum()
                volatility = ret.std() * np.sqrt(ann_factor)
                sharpe = (ret.mean() * ann_factor - rf) / volatility if volatility > 1e-8 else np.nan
                wealth_index = np.exp(cum_returns)
                drawdown = (wealth_index - wealth_index.cummax())/ wealth_index.cummax()
                rows.append({
                    "method": None,
                    "strategy": "EQ",
                    "window": days,
                    "freq": freq,
                    "return": ret.mean() * ann_factor,
                    "volatility": volatility,
                    "sharpe": sharpe,
                    "drawdown": drawdown.min(),
                    "turnover": None
                })
    else:
        for m in method:
            for days in window:
                for freq in rebalance_frequency:
                    ann_factor = {
                        "D": 252,
                        "W": 52,
                        "M": 12
                    }[freq]
                    ret = net_returns[m][days][freq].squeeze()
                    cum_returns = ret.cumsum()
                    volatility = ret.std() * np.sqrt(ann_factor)
                    sharpe = (ret.mean() * ann_factor - rf) / volatility if volatility > 1e-8 else np.nan
                    wealth_index = np.exp(cum_returns)
                    drawdown = (wealth_index - wealth_index.cummax())/ wealth_index.cummax()
                    average_turnover = turnover[m][days][freq].squeeze().mean()
                    rows.append({
                        "method": m,
                        "strategy": kind,
                        "window": days,
                        "freq": freq,
                        "return": ret.mean() * ann_factor,
                        "volatility": volatility,
                        "sharpe": sharpe,
                        "drawdown": drawdown.min(),
                        "turnover": average_turnover
                    })
    metrics = pd.DataFrame(rows)
    assert (metrics["drawdown"] <= 0).all()
    assert metrics["volatility"].min() >= 0
    assert not metrics["sharpe"].isna().all()
    return metrics