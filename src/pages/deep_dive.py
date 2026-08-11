"""Matplotlib deep-dive tab."""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import streamlit as st


def render(fdf):
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
        ax.tick_params(axis="x", rotation=45)
        ax.spines[["top", "right"]].set_visible(False)
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
        ax.spines[["top", "right"]].set_visible(False)
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
        ax.spines[["top", "right"]].set_visible(False)
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
        ax.spines[["top", "right"]].set_visible(False)
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        fig.tight_layout()
        st.pyplot(fig)