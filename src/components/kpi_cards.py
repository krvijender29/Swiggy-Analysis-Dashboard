import streamlit as st

def render_kpi(fdf):
    total_order = len(fdf)
    total_revenue = fdf["Price (INR)"].sum()
    avg_price = fdf["Price (INR)"].mean()
    avg_rating = fdf["Rating"].mean()
    n_restaurants = fdf["Restaurant Name"].nunique()
    n_cities = fdf["City"].nunique()

    kpis = [
        ("Total Orders", f"{total_order:,}","🧾"),
        ("Total Revenue", f"₹{total_revenue/1e7:.2f}Cr","💰"),
        ("Avg. Rating",f"{avg_rating:.2f}⭐","⭐"),
        ("Restaurants", f"{n_restaurants:,}","🍽️"),
        ("Cities Covered", f"{n_cities:,}","🏙️"),
    ]

    cols = st.columns(6)
    for col, (label, value, icon) in zip(cols, kpis):
        with col:
            st.markdown(
                f"""
                <div class ="metric-card">
                    <div class="metric-label">{icon} {label}</div>
                    <div class="metric-card">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,

            )