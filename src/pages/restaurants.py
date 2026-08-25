"""Restaurant intelligence tab — search, leaderboard and unit economics."""
import plotly.express as px
import streamlit as st

from src.config import COLOR_SEQ
from src.utils.chart_helpers import style_fig


def render(fdf):
    st.markdown('<div class="section-header">Restaurant Leaderboard</div>', unsafe_allow_html=True)

    search = st.text_input("Search restaurant", placeholder="e.g. pizza, sweets, sagar…").strip().lower()
    view = fdf
    if search:
        view = fdf[fdf["Restaurant Name"].str.lower().str.contains(search, na=False)]
        if view.empty:
            st.info(f"No restaurants match “{search}” within the current filters.")

    agg = (
        view.groupby("Restaurant Name")
        .agg(
            Orders=("Price (INR)", "count"),
            Revenue=("Price (INR)", "sum"),
            AvgOrderValue=("Price (INR)", "mean"),
            AvgRating=("Rating", "mean"),
            Cities=("City", "nunique"),
            TopLocation=("Location", lambda s: s.value_counts().idxmax()),
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    c1, c2 = st.columns([1.4, 1])
    with c1:
        top_rev = agg.head(10).sort_values("Revenue")
        fig = px.bar(
            top_rev, x="Revenue", y="Restaurant Name", orientation="h",
            color="AvgRating", color_continuous_scale="RdYlGn",
            title="Top 10 Restaurants by Revenue (colored by rating)",
            labels={"Restaurant Name": "Restaurant"},
        )
        st.plotly_chart(style_fig(fig, 480), width="stretch")
    with c2:
        fig = px.scatter(
            agg[agg["Orders"] >= 5], x="AvgOrderValue", y="AvgRating",
            size="Orders", color="Cities", color_continuous_scale=COLOR_SEQ,
            hover_name="Restaurant Name", size_max=42, opacity=0.85,
            title="Unit Economics: AOV vs Rating (bubble = orders)",
        )
        st.plotly_chart(style_fig(fig, 480), width="stretch")

    st.dataframe(
        agg.style.format(
            {
                "Revenue": "₹{:,.0f}",
                "AvgOrderValue": "₹{:,.0f}",
                "AvgRating": "{:.2f} ★",
                "Orders": "{:,}",
            }
        ),
        width="stretch",
        hide_index=True,
        height=420,
    )

    st.markdown('<div class="section-header">Reach & Popularity</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        multi = (
            agg.assign(Cities=agg["Cities"])
            .sort_values(["Cities", "Orders"], ascending=False)
            .head(10)
        )
        fig = px.bar(
            multi, x="Cities", y="Restaurant Name", orientation="h",
            color="Orders", color_continuous_scale="Oranges",
            title="Widest Reach — Cities Covered (top 10)",
            labels={"Restaurant Name": "Restaurant"},
        )
        st.plotly_chart(style_fig(fig, 460), width="stretch")
    with c4:
        loc = view["Location"].value_counts().head(10).reset_index()
        loc.columns = ["Location", "Orders"]
        fig = px.bar(
            loc.sort_values("Orders"), x="Orders", y="Location", orientation="h",
            color="Orders", color_continuous_scale="Oranges",
            title="Top 10 Localities by Orders",
        )
        st.plotly_chart(style_fig(fig, 460), width="stretch")
