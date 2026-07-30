"""
Swiggy Orders Analysis Dashboard
Built with Streamlit, Pandas, NumPy, Plotly & Matplotlib
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Swiggy Analytics Dashboard",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# MODERN STYLING
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: linear-gradient(180deg, #0f1117 0%, #14161f 100%);
    }

    section[data-testid="stSidebar"] {
        background: #171923;
        border-right: 1px solid #2a2d3a;
    }

    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        background: linear-gradient(90deg, #FF6B35 0%, #FF9142 45%, #FFC371 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -1px;
    }
    .hero-sub {
        color: #9096a8;
        font-size: 1.02rem;
        margin-top: -6px;
        margin-bottom: 1.2rem;
    }

    .metric-card {
        background: linear-gradient(145deg, #1b1e2b, #1f2333);
        border: 1px solid #2b2f42;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        transition: transform 0.15s ease, border 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border: 1px solid #FF6B35;
    }
    .metric-label {
        color: #9096a8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: 'Poppins', sans-serif;
        color: #f5f6fa;
        font-size: 1.65rem;
        font-weight: 700;
    }
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 2px;
    }
    .delta-pos { color: #4ade80; }
    .delta-neg { color: #f87171; }

    .section-header {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        color: #f5f6fa;
        margin-top: 2.2rem;
        margin-bottom: 0.6rem;
        padding-left: 12px;
        border-left: 4px solid #FF6B35;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #171923;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #9096a8;
        font-weight: 600;
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #FF6B35, #FF9142) !important;
        color: white !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #2b2f42;
    }

    .stButton>button {
        background: linear-gradient(90deg, #FF6B35, #FF9142);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    .footer-note {
        text-align: center;
        color: #565b6e;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #2a2d3a;
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading Swiggy order data...")
def load_data():
    path = Path(__file__).parent / "data" / "Swiggy_Raw_Data_Excel.xlsx"
    df = pd.read_excel(path)
    df.columns = [c.strip() for c in df.columns]
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Weekday"] = df["Order Date"].dt.day_name()
    df["Week"] = df["Order Date"].dt.isocalendar().week
    # Price buckets
    bins = [0, 100, 200, 300, 500, 1000, np.inf]
    labels = ["<100", "100-200", "200-300", "300-500", "500-1000", "1000+"]
    df["Price Bucket"] = pd.cut(df["Price (INR)"], bins=bins, labels=labels)
    return df


df = load_data()

# ----------------------------------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🧡 Swiggy Analytics")
st.sidebar.markdown("Filter the dataset below")
st.sidebar.markdown("---")

min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
date_range = st.sidebar.date_input(
    "📅 Order Date Range",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

states = sorted(df["State"].unique().tolist())
sel_states = st.sidebar.multiselect("🗺️ State", states, default=[])

city_pool = df[df["State"].isin(sel_states)]["City"].unique() if sel_states else df["City"].unique()
cities = sorted(city_pool.tolist())
sel_cities = st.sidebar.multiselect("🏙️ City", cities, default=[])

price_min, price_max = float(df["Price (INR)"].min()), float(df["Price (INR)"].max())
price_range = st.sidebar.slider(
    "💰 Price Range (INR)",
    min_value=float(np.floor(price_min)),
    max_value=float(np.ceil(price_max)),
    value=(float(np.floor(price_min)), float(np.ceil(price_max))),
)

rating_range = st.sidebar.slider(
    "⭐ Rating Range",
    min_value=float(df["Rating"].min()),
    max_value=float(df["Rating"].max()),
    value=(float(df["Rating"].min()), float(df["Rating"].max())),
    step=0.1,
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Dataset: **{len(df):,}** total orders")
st.sidebar.caption("Built with Streamlit · Pandas · NumPy · Plotly · Matplotlib")

# ----------------------------------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------------------------------
fdf = df.copy()

if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    fdf = fdf[(fdf["Order Date"] >= start) & (fdf["Order Date"] <= end)]

if sel_states:
    fdf = fdf[fdf["State"].isin(sel_states)]
if sel_cities:
    fdf = fdf[fdf["City"].isin(sel_cities)]

fdf = fdf[
    (fdf["Price (INR)"] >= price_range[0]) & (fdf["Price (INR)"] <= price_range[1]) &
    (fdf["Rating"] >= rating_range[0]) & (fdf["Rating"] <= rating_range[1])
]

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<p class="hero-title">Swiggy Orders Analysis Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">A modern, interactive view into food delivery orders across India — '
    'explore pricing, ratings, cities, categories and trends over time.</p>',
    unsafe_allow_html=True,
)

if fdf.empty:
    st.warning("No data matches the current filters. Please adjust your selections.")
    st.stop()

# ----------------------------------------------------------------------------
# KPI METRICS
# ----------------------------------------------------------------------------
total_orders = len(fdf)
total_revenue = fdf["Price (INR)"].sum()
avg_price = fdf["Price (INR)"].mean()
avg_rating = fdf["Rating"].mean()
n_restaurants = fdf["Restaurant Name"].nunique()
n_cities = fdf["City"].nunique()

kpi_cols = st.columns(6)
kpis = [
    ("Total Orders", f"{total_orders:,}", "🧾"),
    ("Total Revenue", f"₹{total_revenue/1e7:.2f}Cr", "💰"),
    ("Avg. Order Value", f"₹{avg_price:,.0f}", "🧮"),
    ("Avg. Rating", f"{avg_rating:.2f} ⭐", "⭐"),
    ("Restaurants", f"{n_restaurants:,}", "🍽️"),
    ("Cities Covered", f"{n_cities:,}", "🏙️"),
]
for col, (label, value, icon) in zip(kpi_cols, kpis):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# PLOTLY THEME
# ----------------------------------------------------------------------------
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQ = ["#FF6B35", "#FF9142", "#FFC371", "#4ecdc4", "#556fb5", "#a685e2", "#f7b267"]

def style_fig(fig, height=420):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#d6d9e3"),
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

# ----------------------------------------------------------------------------
# TABS
# ----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Overview", "🗺️ Geography", "🍛 Categories & Dishes", "⭐ Ratings & Pricing", "📊 Deep Dive (Matplotlib)"]
)

# ============================================================================
# TAB 1 — OVERVIEW
# ============================================================================
with tab1:
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
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        wd = fdf.groupby("Weekday").size().reindex(weekday_order).reset_index(name="Orders")
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

# ============================================================================
# TAB 2 — GEOGRAPHY
# ============================================================================
with tab2:
    st.markdown('<div class="section-header">State & City Performance</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])
    with c1:
        state_agg = fdf.groupby("State").agg(Orders=("Price (INR)", "count"),
                                               Revenue=("Price (INR)", "sum")).reset_index()
        state_agg = state_agg.sort_values("Orders", ascending=False)
        fig = px.bar(state_agg, x="State", y="Orders", color="Revenue",
                     color_continuous_scale="Oranges", title="Orders by State")
        fig.update_layout(xaxis_tickangle=-40)
        st.plotly_chart(style_fig(fig, 460), use_container_width=True)
    with c2:
        fig = px.pie(state_agg.head(8), names="State", values="Orders", hole=0.55,
                     color_discrete_sequence=COLOR_SEQ, title="Order Share — Top 8 States")
        st.plotly_chart(style_fig(fig, 460), use_container_width=True)

    st.markdown('<div class="section-header">Top Cities</div>', unsafe_allow_html=True)
    city_agg = fdf.groupby("City").agg(Orders=("Price (INR)", "count"),
                                        AvgRating=("Rating", "mean"),
                                        Revenue=("Price (INR)", "sum")).reset_index()
    city_agg = city_agg.sort_values("Orders", ascending=False).head(15)
    fig = px.scatter(city_agg, x="Revenue", y="AvgRating", size="Orders", color="City",
                      color_discrete_sequence=COLOR_SEQ, size_max=45,
                      title="City Landscape: Revenue vs. Avg Rating (bubble = order volume)")
    st.plotly_chart(style_fig(fig, 480), use_container_width=True)

    st.dataframe(
        city_agg.rename(columns={"AvgRating": "Avg Rating"}).style.format(
            {"Revenue": "₹{:,.0f}", "Avg Rating": "{:.2f}"}
        ),
        use_container_width=True, hide_index=True
    )

# ============================================================================
# TAB 3 — CATEGORIES & DISHES
# ============================================================================
with tab3:
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
    dish_agg = fdf.groupby("Dish Name").agg(Orders=("Price (INR)", "count"),
                                             AvgPrice=("Price (INR)", "mean"),
                                             AvgRating=("Rating", "mean")).reset_index()
    dish_agg = dish_agg.sort_values("Orders", ascending=False).head(15)
    fig = px.bar(dish_agg.sort_values("Orders"), x="Orders", y="Dish Name", orientation="h",
                 color="AvgRating", color_continuous_scale="RdYlGn", title="Top 15 Dishes by Orders")
    st.plotly_chart(style_fig(fig, 500), use_container_width=True)

# ============================================================================
# TAB 4 — RATINGS & PRICING
# ============================================================================
with tab4:
    st.markdown('<div class="section-header">Rating Distribution</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(fdf, x="Rating", nbins=20, color_discrete_sequence=[COLOR_SEQ[0]],
                            title="Distribution of Ratings")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c2:
        fig = px.box(fdf, x="Price Bucket", y="Rating", color="Price Bucket",
                     color_discrete_sequence=COLOR_SEQ, title="Rating Spread by Price Bucket")
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    st.markdown('<div class="section-header">Price Analysis</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        pb = fdf["Price Bucket"].value_counts().reindex(["<100","100-200","200-300","300-500","500-1000","1000+"]).reset_index()
        pb.columns = ["Price Bucket", "Orders"]
        fig = px.bar(pb, x="Price Bucket", y="Orders", color="Orders", color_continuous_scale="Oranges",
                     title="Orders by Price Bucket")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c4:
        fig = px.scatter(fdf.sample(min(3000, len(fdf)), random_state=1), x="Price (INR)", y="Rating",
                          color="Rating Count", color_continuous_scale="Turbo", opacity=0.6,
                          title="Price vs. Rating (sampled)")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    # Correlation using numpy
    st.markdown('<div class="section-header">Correlation Snapshot (NumPy)</div>', unsafe_allow_html=True)
    corr_cols = ["Price (INR)", "Rating", "Rating Count"]
    corr_matrix = np.corrcoef(fdf[corr_cols].T.values)
    corr_df = pd.DataFrame(corr_matrix, index=corr_cols, columns=corr_cols)
    fig = px.imshow(corr_df, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                     title="Correlation Matrix — Price, Rating, Rating Count")
    st.plotly_chart(style_fig(fig, 420), use_container_width=True)

# ============================================================================
# TAB 5 — MATPLOTLIB DEEP DIVE
# ============================================================================
with tab5:
    st.markdown('<div class="section-header">Static Charts (Matplotlib)</div>', unsafe_allow_html=True)
    st.caption("A couple of classic matplotlib visuals for a print-style analytical view.")

    plt.style.use("dark_background")

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        monthly_np = fdf.groupby("Month")["Price (INR)"].sum()
        ax.plot(monthly_np.index, monthly_np.values, color="#FF6B35", marker="o", linewidth=2.2)
        ax.fill_between(range(len(monthly_np)), monthly_np.values, color="#FF6B35", alpha=0.15)
        ax.set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold", color="white")
        ax.set_ylabel("Revenue (INR)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e5:.1f}L"))
        ax.tick_params(axis='x', rotation=45)
        ax.spines[['top', 'right']].set_visible(False)
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        fig.tight_layout()
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        top_states = fdf["State"].value_counts().head(8)
        colors = plt.cm.Oranges(np.linspace(0.4, 0.95, len(top_states)))
        ax.barh(top_states.index[::-1], top_states.values[::-1], color=colors[::-1])
        ax.set_title("Top 8 States by Order Count", fontsize=13, fontweight="bold", color="white")
        ax.set_xlabel("Orders")
        ax.spines[['top', 'right']].set_visible(False)
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        fig.tight_layout()
        st.pyplot(fig)

    c3, c4 = st.columns(2)
    with c3:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        ax.hist(fdf["Rating"], bins=18, color="#FF9142", edgecolor="#0f1117")
        ax.axvline(fdf["Rating"].mean(), color="#4ecdc4", linestyle="--", linewidth=2,
                   label=f"Mean = {fdf['Rating'].mean():.2f}")
        ax.set_title("Rating Distribution", fontsize=13, fontweight="bold", color="white")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.spines[['top', 'right']].set_visible(False)
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        fig.tight_layout()
        st.pyplot(fig)

    with c4:
        fig, ax = plt.subplots(figsize=(6, 4.2))
        sample = fdf.sample(min(2000, len(fdf)), random_state=1)
        sc = ax.scatter(sample["Price (INR)"], sample["Rating"], c=sample["Rating Count"],
                         cmap="autumn", alpha=0.55, s=18)
        ax.set_title("Price vs. Rating (colored by Rating Count)", fontsize=12, fontweight="bold", color="white")
        ax.set_xlabel("Price (INR)")
        ax.set_ylabel("Rating")
        cbar = fig.colorbar(sc, ax=ax)
        cbar.set_label("Rating Count")
        ax.spines[['top', 'right']].set_visible(False)
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        fig.tight_layout()
        st.pyplot(fig)

# ----------------------------------------------------------------------------
# RAW DATA EXPANDER
# ----------------------------------------------------------------------------
with st.expander("🔍 View Filtered Raw Data"):
    st.dataframe(fdf.drop(columns=["Month", "Weekday", "Week", "Price Bucket"]), use_container_width=True)
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data as CSV", csv, "swiggy_filtered_data.csv", "text/csv")

st.markdown('<div class="footer-note">Swiggy Analytics Dashboard · Built with Streamlit, Pandas, NumPy, Plotly & Matplotlib</div>',
            unsafe_allow_html=True)
