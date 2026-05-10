import numpy as np
import pandas as pd
from src.covariance import covariance_matrix
from src.portfolios import gmv, risk_parity

def rebalacing(returns: pd.DataFrame, window: list, method: list, rebalance_freq: list):
    T = len(returns)
    n = len(returns.columns)
    w_gmv = {m: {date:{freq: [] for freq in rebalance_freq} for date in window} for m in method}
    w_rp = {m: {date:{freq: [] for freq in rebalance_freq} for date in window} for m in method}
    w_eq = {date: [] for date in window}
    r_gmv = {m: {date:{freq: [] for freq in rebalance_freq} for date in window} for m in method}
    r_rp = {m: {date:{freq: [] for freq in rebalance_freq} for date in window} for m in method}
    r_eq = {date: [] for date in window}
    index = {date: {freq: [] for freq in rebalance_freq} for date in window}
    for date in window:
        for freq in rebalance_freq:
            for m in method:
                w_current_gmv = None
                w_current_rp = None
                for time in range(date, T):
                    train = returns.iloc[time-date:time]
                    test = returns.iloc[time]
                    current_date = returns.index[time]
                    if freq == "D":
                        rebalance = True
                    elif freq == "W":
                        rebalance = current_date.weekday() == 4
                    elif freq == "M":
                        if time == date:
                            rebalance = True
                        else:
                            prev_date = returns.index[time-1]
                            rebalance = current_date.month != prev_date.month
                    else:
                        raise ValueError("Rebalance deve essere Giornaliero, Settimanale o Mensile")
                    if (w_current_gmv is None ) or rebalance:
                        matrix = covariance_matrix(train, method = m)
                        w_current_gmv = gmv(matrix)
                        w_current_rp = risk_parity(matrix)
                    r_t_gmv = w_current_gmv @ test
                    r_t_rp= w_current_rp @ test
                    w_gmv[m][date][freq].append(w_current_gmv)
                    w_rp[m][date][freq].append(w_current_rp)
                    r_gmv[m][date][freq].append(r_t_gmv)
                    r_rp[m][date][freq].append(r_t_rp)
                    if m == method[0] and freq == rebalance_freq[0]:
                        w_t_eq = np.ones(n) / n
                        r_t_eq = w_t_eq @ test
                        w_eq[date].append(w_t_eq)
                        r_eq[date].append(r_t_eq)
                    if m == method[0]:
                        index[date][freq].append(current_date)
    w_gmv = {m: {date: {freq: 
                       pd.DataFrame(w_gmv[m][date][freq], columns = returns.columns, index = index[date][freq]) 
                       for freq in rebalance_freq} for date in window} for m in method}
    w_rp = {m: {date: {freq: 
                      pd.DataFrame(w_rp[m][date][freq], columns = returns.columns, index = index[date][freq]) 
                      for freq in rebalance_freq} for date in window} for m in method}
    w_eq = {date: {freq: pd.DataFrame(w_eq[date], columns = returns.columns, index = index[date][freq]) 
                   for freq in rebalance_freq} for date in window}
    r_gmv = {m: {date: {freq: 
                        pd.Series(r_gmv[m][date][freq], index = index[date][freq]) 
                        for freq in rebalance_freq} for date in window} for m in method}
    r_rp = {m: {date: {freq: 
                        pd.Series(r_rp[m][date][freq], index = index[date][freq]) 
                        for freq in rebalance_freq} for date in window} for m in method}
    r_eq = {date: {freq:pd.Series(r_eq[date], index = index[date][freq]) for freq in rebalance_freq} for date in window}
    return w_gmv, w_rp, w_eq, r_gmv, r_rp, r_eq