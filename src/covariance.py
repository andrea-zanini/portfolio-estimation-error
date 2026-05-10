import numpy as np
import pandas as pd
from sklearn.covariance import ledoit_wolf

def covariance_matrix(returns: pd.DataFrame, method: str):
    if method == "Simple":
        matrix: np.ndarray = returns.cov()
    else:
        matrix, shrink = ledoit_wolf(returns.values)
    return matrix