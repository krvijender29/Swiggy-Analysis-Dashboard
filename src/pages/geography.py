import plotly.express as px
import streamlit as st

from src.config import COLOR_SEQ
from src.utils.chart_helpers import style_fig


def render(fdf):
    st.markdown('<div class="section-header">State & City Performance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])
    with c1:
        state_agg = fdf.groupby("State").agg(
            Orders=("Price (INR)", "count"), Revenue=("Price (INR)", "sum")
        ).reset_index().sort_values("Orders", ascending=False)
        fig = px.bar(state_agg, x="State", y="Orders", color="Revenue",
                     color_continuous_scale="Oranges", title="Orders by State")
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(style_fig(fig, 460), width="stretch")
    with c2:
        fig = px.pie(state_agg.head(8), names="State", values="Orders", hole=0.55,
                     color_discrete_sequence=COLOR_SEQ, title="Order Share — Top 8 States")
        st.plotly_chart(style_fig(fig, 460), width="stretch")

    st.markdown('<div class="section-header">Top Cities</div>', unsafe_allow_html=True)
    city_agg = fdf.groupby("City").agg(
        Orders=("Price (INR)", "count"),
        AvgRating=("Rating", "mean"),
        Revenue=("Price (INR)", "sum"),
    ).reset_index().sort_values("Orders", ascending=False).head(15)

    fig = px.scatter(city_agg, x="Revenue", y="AvgRating", size="Orders", color="City",
                      color_discrete_sequence=COLOR_SEQ, size_max=45,
                      title="City Landscape: Revenue vs. Avg Rating (bubble = order volume)")
    st.plotly_chart(style_fig(fig, 480), width="stretch")

    st.dataframe(
        city_agg.rename(columns={"AvgRating": "Avg Rating"}).style.format(
            {"Revenue": "₹{:,.0f}", "Avg Rating": "{:.2f}"}
        ),
        width="stretch", hide_index=True,
    )