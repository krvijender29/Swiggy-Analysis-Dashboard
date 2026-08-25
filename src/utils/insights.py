"""Rule-based auto-insights generated from the filtered dataframe."""
import pandas as pd

from src.config import WEEKDAY_ORDER


def _pct_change(cur: float, prev: float) -> float:
    if prev == 0:
        return 0.0
    return (cur - prev) / prev * 100.0


def build_insights(fdf: pd.DataFrame) -> list[str]:
    if fdf.empty:
        return []

    insights: list[str] = []
    monthly = fdf.groupby("Month").agg(
        Orders=("Price (INR)", "count"), Revenue=("Price (INR)", "sum")
    ).sort_index()

    if len(monthly) >= 2:
        last, prev = monthly.iloc[-1], monthly.iloc[-2]
        o_chg = _pct_change(last["Orders"], prev["Orders"])
        r_chg = _pct_change(last["Revenue"], prev["Revenue"])
        arrow = "📈" if o_chg >= 0 else "📉"
        insights.append(
            f"{arrow} **{monthly.index[-1]}** vs **{monthly.index[-2]}**: orders "
            f"{'up' if o_chg >= 0 else 'down'} **{abs(o_chg):.1f}%**, revenue "
            f"{'up' if r_chg >= 0 else 'down'} **{abs(r_chg):.1f}%**."
        )
    elif len(monthly) == 1:
        insights.append(f"🗓️ Only one month of data in view (**{monthly.index[0]}**) — widen the date range for trends.")

    peak = monthly["Orders"].idxmax()
    insights.append(f"🏆 **{peak}** was the busiest month with **{int(monthly.loc[peak, 'Orders']):,} orders**.")

    wd = fdf["Weekday"].value_counts().reindex(WEEKDAY_ORDER).dropna()
    if not wd.empty:
        best, worst = wd.idxmax(), wd.idxmin()
        share = wd.max() / wd.sum() * 100
        weekend = wd[["Saturday", "Sunday"]].sum() / wd.sum() * 100
        insights.append(
            f"📅 **{best}** drives the most orders ({share:.1f}%); **{worst}** is the quietest day. "
            f"Weekend share: **{weekend:.1f}%**."
        )

    top_state = fdf["State"].value_counts().idxmax()
    top_city = fdf["City"].value_counts().idxmax()
    city_share = fdf["City"].value_counts(normalize=True).max() * 100
    insights.append(
        f"🗺️ **{top_state}** leads among states; **{top_city}** is the top city "
        f"with **{city_share:.1f}%** of all filtered orders."
    )

    cat = fdf["Category"].value_counts()
    if not cat.empty:
        cat_rev = fdf.groupby("Category")["Price (INR)"].sum()
        insights.append(
            f"🍛 Most ordered category: **{cat.idxmax()}** ({cat.max():,} orders); "
            f"highest revenue: **{cat_rev.idxmax()}** (₹{cat_rev.max()/1e5:.1f}L)."
        )

    dish = fdf["Dish Name"].value_counts()
    if not dish.empty:
        insights.append(f"🍲 Best-selling dish: **{dish.idxmax()}** with **{dish.max():,} orders**.")

    bucket = fdf["Price Bucket"].value_counts()
    if not bucket.empty:
        insights.append(
            f"💰 Preferred price band: **{bucket.idxmax()} INR** accounting for "
            f"**{bucket.max()/len(fdf)*100:.1f}%** of orders."
        )

    hi = fdf[fdf["Rating"] >= 4.5]
    insights.append(
        f"⭐ Average rating is **{fdf['Rating'].mean():.2f}**; **{len(hi)/len(fdf)*100:.1f}%** of orders "
        f"come from restaurants rated 4.5+."
    )

    rest = fdf["Restaurant Name"].value_counts()
    if not rest.empty:
        insights.append(
            f"🍽️ Top restaurant: **{rest.idxmax()}** with **{rest.max():,} orders** across "
            f"**{fdf[fdf['Restaurant Name'] == rest.idxmax()]['City'].nunique()}** cities."
        )

    return insights
