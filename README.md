Portfolio Optimization under Estimation Error

Overview

This project analyzes the impact of covariance estimation error on portfolio optimization.
The goal is to isolate the impact of estimation error on portfolio performance.

I compare three allocation strategies:

* Global Minimum Variance (GMV)
* Risk Parity (RP)
* Equal Weight (EQ)

under different configurations:

* covariance estimation: sample vs shrinkage (Ledoit-Wolf)
* rolling window length: 60, 120, 252 days
* rebalancing frequency: daily, weekly, monthly
* transaction costs included
* 1-year risk-free rate

⸻

Key Idea

Portfolio optimization is highly sensitive to estimation error.

In particular:

* GMV relies on the inverse of the covariance matrix
* estimation noise leads to unstable inversion and thus extreme weights
* shrinkage reduces noise and improves stability
* simpler strategies (RP, EQ) are more robust out-of-sample

⸻

Methodology

* Data: daily log returns from 20 US large-cap equities
* rolling window estimation
* out-of-sample backtesting
* using pseudo-inverse in GMV to handle ill-conditioned covariance matrices
* transaction costs modeled via portfolio turnover
* Sharpe ratios are computed using a 1-year risk-free rate, aligned with the return frequency

All strategies are evaluated under the same pipeline to isolate the effect of the allocation method.

⸻

Problems faced

* SLSQP stagnation when solving GMV numerically: switched to closed-form solution
* numerical instability with small windows (60 days) leading to highly concentrated and unstable weights
* initial implementation based on nested Python structures (lists/dictionaries), later refactored into structured pandas DataFrames at output stage
* Excel files (.xlsx) were inefficient for large data: switched to Parquet format for faster I/O while preserving structure

––––

Results

Main findings:

* GMV (sample covariance) shows unstable behavior and poor out-of-sample performance
* GMV (sample covariance) weights become highly concentrated, especially with shorter estimation windows.
* Shrinkage (Ledoit-Wolf) improves performance: violation rate from 20% to 6%
* Risk Parity produces more stable allocations than GMV
* Equal Weight remains a strong benchmark due to zero estimation error

Empirical validation:

* GMV violation rate vs EQ decreases substantially with shrinkage
* turnover behaves consistently across rebalancing frequencies

Trade-off:

* shrinkage: reduces estimation variance by shrinking the covariance matrix toward a structured target, at the cost of introducing bias
* costs: high turnover significantly penalizes GMV strategies
* frequency: more frequent rebalancing increases costs and can reduce net performance

⸻

Metrics

Performance is evaluated using:

* annualized return
* annualized volatility
* Sharpe ratio
* maximum drawdown
* average turnover

⸻

Tech Stack

* Python
* pandas, numpy
* scipy (optimization)
* scikit-learn (Ledoit-Wolf shrinkage)
* matplotlib / seaborn

⸻

Structure

* src/ → core logic (data, covariance, portfolios, backtest, test, metrics, plot)
* results/ → saved weights, returns, turnover, plots, tables
* main.py → data generation and backtest
* notebooks/ → analysis and visualization
**Note**: the `results/` folder contains only plots. 
Data files (.parquet) are excluded from the repository as they are 
fully reproducible by running `src/cleaning.py` followed by `main.py`.

⸻

Limitations

* results depend on the chosen asset universe (US large-cap equities)
* transaction costs are constant (linear model)
* transaction costs are likely overestimated: no sensitivity analysis on transaction costs
* covariance estimation remains noisy even with shrinkage
* RP optimization may be affected by numerical issues

⸻

Takeaway

* Reducing estimation error is more important than increasing model complexity.
* Simple and robust strategies can outperform theoretically optimal ones when inputs are noisy.

⸻

For a detailed technical discussion, see docs/technical_report.pdf