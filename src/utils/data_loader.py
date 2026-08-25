import pandas as pd
import streamlit as st

from src.config import DATA_PATH, PRICE_BINS, PRICE_LABELS


@st.cache_data(show_spinner="Loading Swiggy order data...")
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Weekday"] = df["Order Date"].dt.day_name()
    df["Week"] = df["Order Date"].dt.isocalendar().week
    df["Price Bucket"] = pd.cut(df["Price (INR)"], bins=PRICE_BINS, labels=PRICE_LABELS)
    return df


def filter_data(
        df: pd.DataFrame,
        date_range,
        states: list,
        cities: list,
        price_range: tuple,
        rating_range: tuple,
) -> pd.DataFrame:
    fdf = df.copy()

    if date_range:
        start = pd.to_datetime(date_range[0])
        end = pd.to_datetime(date_range[-1])
        fdf = fdf[(fdf["Order Date"] >= start) & (fdf["Order Date"] <= end)]

    if states:
        fdf = fdf[fdf["State"].isin([s.strip() for s in states])]
    if cities:
        fdf = fdf[fdf["City"].isin([c.strip() for c in cities])]

    if price_range:
        fdf = fdf[
            (fdf["Price (INR)"] >= price_range[0]) & (fdf["Price (INR)"] <= price_range[1])
        ]
    if rating_range:
        fdf = fdf[
            (fdf["Rating"] >= rating_range[0]) & (fdf["Rating"] <= rating_range[1])
        ]
    return fdf