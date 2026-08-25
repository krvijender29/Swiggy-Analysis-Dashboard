# Swiggy Analytics Dashboard

An interactive Streamlit dashboard for exploring Swiggy food-delivery orders across India — pricing, ratings, cities, categories, and trends over time.

## Features

- **📈 Overview** — monthly orders/revenue trends, weekday patterns, top restaurants
- **🗺️ Geography** — state & city breakdowns, bubble chart of revenue vs rating
- **🍛 Categories & Dishes** — top categories, revenue treemap, top dishes
- **⭐ Ratings & Pricing** — rating distribution, price buckets, price-vs-rating scatter, correlation heatmap
- **🍽️ Restaurants** — searchable restaurant leaderboard with revenue/AOV/rating, unit-economics scatter, locality hotspots
- **📊 Deep Dive** — static Matplotlib charts for a print-style analytical view
- **Sidebar filters** — date range, state, city, price range, rating range
- **CSV export** — download the currently filtered data
- **🔮 Auto Insights** — rule-based takeaways (MoM changes, peak days, best sellers) generated from the current filter
- **Revenue forecast** — linear-trend projection of the next 3 months with a ±10% band

Built with Streamlit, Plotly, and Pandas; the Deep Dive tab uses Matplotlib.

## Setup

Requires Python 3.10+.

```bash
# optional: create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## Data

The dataset is expected at `data/Swiggy_Raw_Data_Excel.xlsx` (already included in this repo). To use your own data, either replace that file or update the path in `load_data()` in `src/utils/data_loader.py`.

## Project Structure

```
├── app.py                  # Entry point: layout, filters, tabs
├── requirements.txt
├── data/                   # Raw Excel dataset
└── src/
    ├── config.py           # Page title/icon/layout settings
    ├── styles.py           # Custom CSS styling
    ├── components/         # Sidebar filters, KPI cards
    ├── pages/              # One module per dashboard tab
    └── utils/              # Data loading, filtering, insights and forecast helpers
```
