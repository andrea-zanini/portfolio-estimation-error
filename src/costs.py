def turnover(weight_gmv: dict, weight_risk_parity: dict, window: list, method: list, rebalance_feq: list):
    turnover_gmv = {m: {day: {} for day in window} for m in method}
    turnover_rp = {m: {day: {} for day in window} for m in method}
    for m in method:
        for day in window:
            for freq in rebalance_feq:
                t_g = (weight_gmv[m][day][freq].diff().abs().sum(axis = 1))
                t_rp = weight_risk_parity[m][day][freq].diff().abs().sum(axis = 1)
                turnover_gmv[m][day][freq] = t_g / 2
                turnover_rp[m][day][freq] = t_rp / 2
    return turnover_gmv, turnover_rp

def compute_returns(r_gmv: dict, r_rp: dict, turnover_gmv: dict, turnover_rp: dict, 
                    window: list, method: list, rebalance_feq: list, cost: float):
    net_gmv = {m: {day: {} for day in window} for m in method}
    net_rp = {m: {day: {} for day in window} for m in method}
    for m in method:
        for day in window:
            for freq in rebalance_feq:
                net_gmv[m][day][freq] = r_gmv[m][day][freq] - (turnover_gmv[m][day][freq] * cost)
                net_rp[m][day][freq] = r_rp[m][day][freq] - (turnover_rp[m][day][freq] * cost)
    return net_gmv, net_rp