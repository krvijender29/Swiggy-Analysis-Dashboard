"""Ratings & Pricing tab."""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import COLOR_SEQ
from src.utils.chart_helpers import style_fig


def render(fdf):
    st.markdown('<div class="section-header">Rating Distribution</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(fdf, x="Rating", nbins=20, color_discrete_sequence=[COLOR_SEQ[0]],
                            title="Distribution of Ratings")
        st.plotly_chart(style_fig(fig), width="stretch")
    with c2:
        fig = px.box(fdf, x="Price Bucket", y="Rating", color="Price Bucket",
                     color_discrete_sequence=COLOR_SEQ, title="Rating Spread by Price Bucket")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig), width="stretch")

    st.markdown('<div class="section-header">Price Analysis</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        pb = fdf["Price Bucket"].value_counts().reindex(
            ["<100", "100-200", "200-300", "300-500", "500-1000", "1000+"]
        ).reset_index()
        pb.columns = ["Price Bucket", "Orders"]
        fig = px.bar(pb, x="Price Bucket", y="Orders", color="Orders", color_continuous_scale="Oranges",
                     title="Orders by Price Bucket")
        st.plotly_chart(style_fig(fig), width="stretch")
    with c4:
        sample = fdf.sample(min(3000, len(fdf)), random_state=1)
        fig = px.scatter(sample, x="Price (INR)", y="Rating", color="Rating Count",
                          color_continuous_scale="Turbo", opacity=0.6, title="Price vs. Rating (sampled)")
        st.plotly_chart(style_fig(fig), width="stretch")

    st.markdown('<div class="section-header">Correlation Snapshot (NumPy)</div>', unsafe_allow_html=True)
    corr_cols = ["Price (INR)", "Rating", "Rating Count"]
    corr_matrix = np.corrcoef(fdf[corr_cols].T.values)
    corr_df = pd.DataFrame(corr_matrix, index=corr_cols, columns=corr_cols)
    fig = px.imshow(corr_df, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                     title="Correlation Matrix — Price, Rating, Rating Count")
    st.plotly_chart(style_fig(fig, 420), width="stretch")