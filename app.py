"""Swiggy Orders Analysis Dashboard — main entry point."""
import streamlit as st

from src.config import PAGE_TITLE, PAGE_ICON, LAYOUT
from src.styles import apply_custom_style
from src.utils.data_loader import load_data, filter_data
from src.components.sidebar import render_sidebar
from src.components.kpi_cards import render_kpis
from src.pages import overview, geography, categories, ratings_pricing, deep_dive

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT, initial_sidebar_state="expanded")
apply_custom_style()

df = load_data()

date_range, sel_states, sel_cities, price_range, rating_range = render_sidebar(df)
fdf = filter_data(df, date_range, sel_states, sel_cities, price_range, rating_range)

st.markdown('<p class="hero-title">Swiggy Orders Analysis Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">A modern, interactive view into food delivery orders across India — '
    'explore pricing, ratings, cities, categories and trends over time.</p>',
    unsafe_allow_html=True,
)

if fdf.empty:
    st.warning("No data matches the current filters. Please adjust your selections.")
    st.stop()

render_kpis(fdf)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Overview", "🗺️ Geography", "🍛 Categories & Dishes", "⭐ Ratings & Pricing", "📊 Deep Dive (Matplotlib)"]
)

with tab1:
    overview.render(fdf)
with tab2:
    geography.render(fdf)
with tab3:
    categories.render(fdf)
with tab4:
    ratings_pricing.render(fdf)
with tab5:
    deep_dive.render(fdf)

with st.expander("🔍 View Filtered Raw Data"):
    st.dataframe(fdf.drop(columns=["Month", "Weekday", "Week", "Price Bucket"]), use_container_width=True)
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data as CSV", csv, "swiggy_filtered_data.csv", "text/csv")

st.markdown(
    '<div class="footer-note">Swiggy Analytics Dashboard · Built with Streamlit, Pandas, NumPy, Plotly & Matplotlib</div>',
    unsafe_allow_html=True,
)