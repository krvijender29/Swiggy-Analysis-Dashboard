"""Lightweight linear-trend forecast for monthly order/revenue series."""
import numpy as np
import pandas as pd

HORIZON = 3


def forecast_monthly(monthly: pd.Series, horizon: int = HORIZON) -> pd.DataFrame:
    """Fit a least-squares trend to a monthly series and extend it.

    Returns a dataframe indexed by 'YYYY-MM' with columns [actual, forecast].
    """
    s = monthly.dropna().astype(float).sort_index()
    if len(s) < 2:
        return pd.DataFrame({"actual": s, "forecast": np.nan})

    x = np.arange(len(s), dtype=float)
    slope, intercept = np.polyfit(x, s.values, 1)

    fut_x = np.arange(len(s), len(s) + horizon, dtype=float)
    fut_vals = intercept + slope * fut_x

    last_period = pd.Period(s.index[-1], freq="M")
    fut_idx = [(last_period + i + 1).strftime("%Y-%m") for i in range(horizon)]

    out = pd.DataFrame(
        {
            "actual": list(s.values) + [np.nan] * horizon,
            "forecast": [np.nan] * (len(s) - 1) + [s.values[-1]] + list(fut_vals),
        },
        index=list(s.index) + fut_idx,
    )
    out.index.name = "Month"
    return out


def trend_summary(forecast_df: pd.DataFrame, value_name: str = "orders") -> str | None:
    """One-line takeaway about the projected trend."""
    fc = forecast_df["forecast"].dropna()
    if len(fc) < 2:
        return None
    slope_per_month = fc.iloc[-1] - fc.iloc[-2]
    total_next = fc.iloc[1:].sum()
    direction = "grow" if slope_per_month >= 0 else "decline"
    return (
        f"Trend model expects {value_name} to **{direction} by ~{abs(slope_per_month):,.0f}/month**; "
        f"projected next full month ≈ **{fc.iloc[-1]:,.0f}**, 3-month total ≈ **{total_next:,.0f}**."
    )
