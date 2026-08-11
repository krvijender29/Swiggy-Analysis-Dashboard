import plotly.express as px
import streamlit as st

from src.config import COLOR_SEQ, WEEKDAY_ORDER
from src.utils.chart_helper import style_fig


def render(fdf):
    st.markdown('<div class="section-header">Orders & Revenue Over Time</div>', unsafe_allow_html=True)

    monthly = fdf.groupby("Month").agg(
        Orders=("Price (INR)", "count"),
        Revenue=("Price (INR)", "sum"),
        AvgPrice=("Price (INR)", "mean"),
    ).reset_index().sort_values("Month")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(monthly, x="Month", y="Orders", color_discrete_sequence=[COLOR_SEQ[0]],
                     title="Monthly Order Volume")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c2:
        fig = px.line(monthly, x="Month", y="Revenue", markers=True,
                       color_discrete_sequence=[COLOR_SEQ[1]], title="Monthly Revenue (INR)")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        wd = fdf.groupby("Weekday").size().reindex(WEEKDAY_ORDER).reset_index(name="Orders")
        fig = px.bar(wd, x="Weekday", y="Orders", color="Orders", color_continuous_scale="Oranges",
                     title="Orders by Day of Week")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c4:
        fig = px.line(monthly, x="Month", y="AvgPrice", markers=True,
                       color_discrete_sequence=[COLOR_SEQ[3]], title="Average Order Value Trend")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    st.markdown('<div class="section-header">Top Restaurants by Orders</div>', unsafe_allow_html=True)
    top_r = fdf["Restaurant Name"].value_counts().head(10).reset_index()
    top_r.columns = ["Restaurant", "Orders"]
    fig = px.bar(top_r.sort_values("Orders"), x="Orders", y="Restaurant", orientation="h",
                 color="Orders", color_continuous_scale="Sunsetdark", title="Top 10 Restaurants")
    st.plotly_chart(style_fig(fig, 460), use_container_width=True)