import yfinance as yf
import pandas as pd
import numpy as np
def get_data(names: list, horizon: str, time: str):
    data: pd.DataFrame = yf.download(tickers = names, period= horizon, interval = time, auto_adjust = False, )
    if "Adj Close" in data:
        price: pd.DataFrame = data["Adj Close"]
    else:
        price=data["Close"]
    if price.isna().sum().sum() > 0:
        price.ffill(inplace = True)
        price.bfill(inplace = True)
        price.dropna(inplace = True, axis = 1, how = "any")
    price.index = pd.to_datetime(price.index)
    returns: pd.DataFrame = np.log(price).diff().dropna()
    return returns