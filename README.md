# Polymarket FAA Attribution Forecasting (02)

Forecasts 4-hour ahead attribution probabilities using persistence and volatility scaling.
- Median: Persistent last known market price.
- Volatility: Population standard deviation of 1-minute price changes over the last 360 minutes (scaled by 0.35, floored at 0.0002, capped at 0.004).
- Quantiles: Normal distribution quantiles scaled by square root of horizon minutes, clamped to [0, 1], rounded to 6 decimals, and enforced non-decreasing.
