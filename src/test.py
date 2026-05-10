import pandas as pd
import numpy as np

def check_weights(w):
    assert not w.isna().any().any()
    assert (w.sum(axis=1) - 1).abs().max() < 1e-8

def delta(w):
    return w.diff().abs().sum(axis = 1), w.max()

def check_gmv(w_df, returns, window = 60):
    violations = 0
    for i in range(window, len(w_df)):
        w = w_df.iloc[i]
        sigma = returns.iloc[i-window:i].cov()
        sigma = sigma.loc[w.index, w.index]
        w_eq = pd.Series(1 / len(w), index=w.index)
        lhs = w.values @ sigma.values @ w.values
        rhs = w_eq.values @ sigma.values @ w_eq.values
        if lhs > rhs:
            violations += 1
    assert violations / len(w_df) < 0.05

def turnover_check(turnover):
    d = turnover["D"].dropna().mean()
    w = turnover["W"].dropna().mean()
    m = turnover["M"].dropna().mean()
    assert d > w > m

def gmv_vs_eq_violation_rate(w_df, returns, window = 60):
    violations = 0
    for i in range(window, len(w_df)):
        w = w_df.iloc[i]
        sigma = returns.iloc[i-window:i].cov()
        sigma = sigma.loc[w.index, w.index]
        w_eq = np.ones(len(w)) / len(w)
        lhs = w.values @ sigma.values @ w.values
        rhs = w_eq @ sigma.values @ w_eq
        if lhs > rhs:
            violations += 1
    return violations / len(w_df)