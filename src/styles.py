import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

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
"""


def apply_custom_style():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)