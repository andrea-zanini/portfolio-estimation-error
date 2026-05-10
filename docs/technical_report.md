Portfolio Optimization under Estimation Error

⸻

1. Objective

This project investigates how estimation error in the covariance matrix affects portfolio optimization.

The focus is on comparing:

* Global Minimum Variance (GMV)
* Risk Parity (RP)
* Equal Weight (EQ)

under realistic constraints:

* rolling window estimation
* transaction costs
* Sharpe ratio comupted using 1-year risk-free rates
* different rebalancing frequencies

⸻

2. Theoretical Background

GMV

The GMV portfolio solves:
$$
w^* = \frac{\Sigma^{-1} \mathbf{1}}{\mathbf{1}^T \Sigma^{-1} \mathbf{1}}
$$
Key issue:

* depends on \Sigma^{-1}
* with limited sample size (e.g 60 days for 20 assets) the estimation error becomes significant
* estimation errors are amplified through matrix inversion, leading to large distorsion in portfolio weights
* The pseudo-inverse is used to handle near-singular or ill-conditioned covariance matrices, but it doesn't address the underlying estimation error

⸻

Risk Parity

Risk Parity allocates weights such that:

$$
w_i (\Sigma w)_i = \frac{1}{n} w^T \Sigma w
$$

Properties:

* no matrix inversion
* relies on numerical optimization
* implicitly depends on covariance structure through marginal risk contributions
* more stable under noisy inputs
* implemented via constrained numerical optimization (e.g. SLSQP with budget and bound constraints)
⸻

Equal Weight

$$
w_i = \frac{1}{n}
$$

* no estimation
* robust baseline

⸻

Shrinkage (Ledoit-Wolf)

To reduce noise:
$$
\hat{\Sigma} = \delta F + (1 - \delta) S
$$
where:

* S: sample covariance
* F: structured target (diagonal)

Trade-off:

* improves stability
* shrinks the covariance matrix toward a structured target
* it reduces estimation variance at the cost of introducing bias

⸻

3. Methodology

Data

* 20 US large-cap equities
* daily log returns
* 10-year horizon

⸻

Backtest

* rolling window: 60, 120, 252 days
* rebalancing: daily, weekly, monthly
* out-of-sample evaluation

Weights computed using past data (up to time t-1) are applied to returns at time t.

⸻

Transaction Costs

Modeled as:
$$
r^{net}_t = r_t - c \cdot \text{turnover}_t
$$
with turnover defined as:
$$
(\sum_i |w_{t,i} - w_{t-1,i}|)/2
$$

Note:

* this may overestimate or underestimate costs, as no sensitivity analysis across volatility regimes is performed

⸻

4. Implementation Notes

* GMV computed in closed form
* RP solved via SLSQP with constraints
* fallback to equal weights when optimization fails

Observed issues:

* SLSQP stagnation when solving GMV numerically: switched to closed-form solution
* numerical instability with small windows (60 days): extreme weights are observed
* initial implementation based on nested Python structures, later refactored into structured pandas DataFrames at output stage
* Excel files (.xlsx) were inefficient for large data: switched to Parquet format for faster I/O while preserving structure

⸻

5. Validation

Sanity checks:

* weights sum to 1
* no missing values
* turnover consistency:
    $$
    \text{Turnover: Daily} > \text{Weekly} > \text{Monthly}
    $$
* monitoring of weight concentration and instability (via max weights and weight changes)

GMV validation:

* compared against Equal Weight
* violation rate (GMV variance > EQ variance) used as diagnostic
* this metrics captures how often GMV fails to outperform a naive benchmark under estimation error.
* this effect is particularly severe when the covariance matrix is ill-conditioned

Note:

* a direct GMV optimality check was initially implemented but discarded due to instability under estimation error

Observed:

* sample covariance: ~20% violations
* shrinkage: ~6% violations

⸻

6. Results

Main findings

* GMV (sample covariance):
    * unstable behavior
    * poor out-of-sample performance
    * weights are highly concentrated
    * high sensitivity to noise
    

* GMV (shrinkage):
    * improved stability
    * lower violation rate

* Risk Parity:
    * no matrix inversion, less sensitive to estimation error
    * optimization still depends on covariance
    * stability observed in lower turnover and less concentration
    
* Equal Weight:
    * competitive benchmark
    * robust due to absence of estimation

⸻

Effect of Rebalancing

* higher frequency implies higher turnover
* transaction costs significantly impact performance

⸻

Effect of Window Length

* short windows:
    * high estimation noise
    
* long windows:
    * more stable but less reactive

––––

Economic Interpretation

* Why GMV fails:
    * the covariance matrix is estimated with noise
    * matrix inversion amplifies estimation errors
    * assets with underestimated variance receive excessively large weights
    * this leads to unstable and highly concentrated portfolios
    * the model isn't wrong, but the inputs are too noisy relative to the dimensionality of the problem
    
* Why shrinkage helps:
    * reduces estimation noise in covariance and correlations
    * shrinks the matrix toward a structured target (diagonal)
    * improves numerical stability of the inversion
    * introduces a bias–variance trade-off (more bias, less variance)
    
* Why Equal Weight works:
    * no covariance estimation is required
    * no estimation error is introduced
    * acts as a robust baseline despite being biased

⸻

7. Limitations

* results depend on the chosen asset universe (US large-cap equities)
* transaction costs are constant (linear model)
* transaction costs may be misestimated due to the simplified linear model and absence of market microstructure effects
* covariance estimation remains noisy even with shrinkage
* RP optimization may be affected by numerical issues

⸻

8. Conclusion

* Estimation error dominates portfolio optimization, particularly in high-dimensional settings with limited data

Key takeaway:

* reducing input noise is more important than increasing model complexity

In practice:

* shrinkage improves GMV
* RP offers a robust alternative
* simple strategies like Equal Weight remain strong baselines