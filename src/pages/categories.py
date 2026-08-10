import plotly.express as px
import streamlit as st

from src.utils.chart_helpers import style_fig


def render(fdf):
    st.markdown('<div class="section-header">Popular Categories</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        cat_agg = fdf["Category"].value_counts().head(12).reset_index()
        cat_agg.columns = ["Category", "Orders"]
        fig = px.bar(cat_agg.sort_values("Orders"), x="Orders", y="Category", orientation="h",
                     color="Orders", color_continuous_scale="Oranges", title="Top 12 Categories by Orders")
        st.plotly_chart(style_fig(fig, 460), use_container_width=True)
    with c2:
        cat_rev = fdf.groupby("Category")["Price (INR)"].sum().sort_values(ascending=False).head(12).reset_index()
        fig = px.treemap(cat_rev, path=["Category"], values="Price (INR)",
                          color="Price (INR)", color_continuous_scale="Sunsetdark",
                          title="Revenue Share by Category (Top 12)")
        st.plotly_chart(style_fig(fig, 460), use_container_width=True)

    st.markdown('<div class="section-header">Top Dishes</div>', unsafe_allow_html=True)
    dish_agg = fdf.groupby("Dish Name").agg(
        Orders=("Price (INR)", "count"),
        AvgPrice=("Price (INR)", "mean"),
        AvgRating=("Rating", "mean"),
    ).reset_index().sort_values("Orders", ascending=False).head(15)

    fig = px.bar(dish_agg.sort_values("Orders"), x="Orders", y="Dish Name", orientation="h",
                 color="AvgRating", color_continuous_scale="RdYlGn", title="Top 15 Dishes by Orders")
    st.plotly_chart(style_fig(fig, 500), use_container_width=True)