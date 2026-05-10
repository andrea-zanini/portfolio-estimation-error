import numpy as np
from scipy import linalg
from scipy import optimize

def gmv(storical_covariance_matrix):
    matrix: np.ndarray = np.asanyarray(storical_covariance_matrix)
    n = matrix.shape[0]
    one = np.ones(n)
    sigma = linalg.pinv(matrix)
    weights = (sigma @ one) / (one @ sigma @ one)
    return weights

def risk_parity(shrink_covariance_matrix):
    sigma: np.ndarray = np.asanyarray(shrink_covariance_matrix)
    n = sigma.shape[0]
    def objective(w):
        portfolio_var = w @ sigma @ w
        marginal = sigma @ w
        risk_contrib = w * marginal / portfolio_var
        target = 1 / n
        return np.sum((risk_contrib - target)**2)
    x0 = np.ones(n) / n
    constraint = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    bound = tuple((0,1) for i in range(n))
    weights = optimize.minimize(objective, x0,  method = "SLSQP", bounds = bound, constraints = constraint)
    if not weights.success:
        return x0
    return weights.x