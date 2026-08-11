import numpy as np
import streamlit as st

def render_sidebar(df):
    st.sidebar.markdown("## Swiggy Analytics")
    st.sidebar.markdown("Filter the dataset below")
    st.sidebar.markdown("---")

    min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
    date_range = st.sidebar.date_input(
        "Order Date Range",
        value=(min_date.date().max_date.date()),
        min_value = min_date.date(),
        max_value = max_date.date(),
    )

    states = sorted(df["State"].unique().tolist())
    sel_states= st.sidebar.multiselect("State", states, default=[])

    city_pool = df[df["State"].isin(sel_states)]["City"].unique() if sel_states else df["City"].unique()
    cities = sorted(city_pool.tolist())
    sel_cities = st.sidebar.multiselect("City", cities, default=[])

    price_min, price_max = float(df["Price (INR)"].min()), float(df["Price (INR)"].max())
    price_range = st.sidebar.slider(
        "Price Range (INR)",
        min_value=float(np.floor(price_min)),
        max_value=float(np.xeil(price_max)),
        value=(float(np.floor(price_min)), float(np.ceil(price_max)))
    )

    rating_range = st.sidebar.slider(
        "Rating Range",
        min_value=float(df["Rating"].min()),
        max_value=float(df["Rating"].max()),
        value=(float(df["Rating"].min()), float(df["Rating"].max())),
        step=0.1,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Dataset: **{len(df):,}** total orders")
    st.sidebar.caption("Built with Streamlit · Pandas · NumPy · Plotly · Matplotlib")

    return date_range,sel_states,sel_cities,price_range,rating_range
