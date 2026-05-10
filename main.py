from pathlib import Path
from config import tickers, periods, frequency, methods, windows, rebalance_freq, cost_rate
from src.data import get_data
from src.backtest import rebalacing
from src.costs import turnover, compute_returns
from src.test import check_weights, delta, check_gmv, turnover_check, gmv_vs_eq_violation_rate

BASE_DIR = Path(__file__).resolve().parent
weights_path = BASE_DIR / "results" / "weights"
returns_path = BASE_DIR / "results" / "returns"
turnover_path = BASE_DIR / "results" / "turnover"
weights_path.mkdir(parents = True, exist_ok = True)
returns_path.mkdir(parents = True, exist_ok = True)
turnover_path.mkdir(parents = True, exist_ok = True)

log_returns = get_data(names = tickers, horizon = periods, time = frequency)
w_gmv, w_rp, w_eq, r_gmv, r_rp, r_eq = rebalacing(log_returns, windows, methods, rebalance_freq)
turnover_gmv, turnover_rp = turnover(w_gmv, w_rp, windows, methods, rebalance_freq)
net_gmv, net_rp = compute_returns(r_gmv, r_rp, turnover_gmv, turnover_rp, windows, methods, rebalance_freq, cost_rate)

check_weights(w_gmv["Simple"][60]["D"])
delta_w, max_w = delta(w_gmv["Simple"][60]["W"])
print(delta_w)
print(max_w)
turnover_check(turnover_gmv["Simple"][60])
# check_gmv(w_gmv["Simple"][60]["D"], log_returns)
v_simple = gmv_vs_eq_violation_rate(w_gmv["Simple"][60]["D"], log_returns)
v_shrink = gmv_vs_eq_violation_rate(w_gmv["Shrinks"][60]["D"], log_returns)
print(v_simple, v_shrink)

for m in methods:
    for w in windows:
        for f in rebalance_freq:
            w_gmv[m][w][f].to_parquet(weights_path / f"gmv_{m}_w{w}_{f}.parquet")
            w_rp[m][w][f].to_parquet(weights_path / f"rp_{m}_w{w}_{f}.parquet")
            w_eq[w][f].to_parquet(weights_path / f"eq_w{w}_{f}.parquet")

            net_gmv[m][w][f].to_frame("returns")\
                .to_parquet(returns_path / f"gmv_{m}_w{w}_{f}.parquet")
            net_rp[m][w][f].to_frame("returns")\
                .to_parquet(returns_path / f"rp_{m}_w{w}_{f}.parquet")
            r_eq[w][f].to_frame("returns")\
                .to_parquet(returns_path / f"eq_w{w}_{f}.parquet")

            turnover_gmv[m][w][f].to_frame("returns")\
                .to_parquet(turnover_path / f"gmv_{m}_w{w}_{f}.parquet")
            turnover_rp[m][w][f].to_frame("returns")\
                .to_parquet(turnover_path / f"rp_{m}_w{w}_{f}.parquet")