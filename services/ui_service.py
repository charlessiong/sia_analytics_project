# ============================================================
# ui_service.py – Singapore Airlines Clean LIGHT UI (FIXED)
# ============================================================

import streamlit as st

# ============================================================
# COLOR PALETTE (LIGHT & SAFE)
# ============================================================

PRIMARY_NAVY = "#0E3A8A"       # lighter navy (FIX)
ACCENT_GOLD = "#FFED4D"
BACKGROUND_CREAM = "#F5F3EE"
TEXT_GREY = "#555555"

CARD_BG = "#FFFFFF"
CARD_BORDER = "#E5E7EB"


# ============================================================
# GLOBAL STYLE INJECTION (NO DARK SIDEBAR)
# ============================================================

def apply_global_styles():
    st.markdown(
        f"""
<style>

/* ===============================
   App Background
   =============================== */
.stApp {{
    background-color: {BACKGROUND_CREAM} !important;
}}

/* ===============================
   Main Content Padding
   =============================== */
.block-container {{
    padding: 2.5rem 3rem 3rem 3rem;
}}

/* ===============================
   Headings
   =============================== */
h1, h2, h3 {{
    color: {PRIMARY_NAVY} !important;
    font-weight: 800 !important;
}}

h4, h5 {{
    color: {PRIMARY_NAVY} !important;
    font-weight: 700 !important;
}}

/* ===============================
   Text
   =============================== */
p, li {{
    color: {TEXT_GREY} !important;
    font-size: 1.05rem;
}}

/* ===============================
   CARDS
   =============================== */
.sia-card {{
    background: {CARD_BG};
    padding: 1.4rem 1.6rem;
    border-radius: 16px;
    border: 1px solid {CARD_BORDER};
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);

    min-height: 210px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.sia-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.12);
}}

/* ===============================
   Card Text
   =============================== */
.sia-card-title {{
    color: {PRIMARY_NAVY};
    font-size: 1.4rem;
    font-weight: 800;
}}

.sia-card-desc {{
    color: {TEXT_GREY};
    font-size: 1rem;
}}

/* ===============================
   Metrics
   =============================== */
[data-testid="stMetricValue"] {{
    color: {PRIMARY_NAVY} !important;
    font-weight: 800 !important;
}}

/* ===============================
   Buttons
   =============================== */
.stButton > button {{
    background-color: {PRIMARY_NAVY};
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    border: none;
}}

.stButton > button:hover {{
    background-color: {ACCENT_GOLD};
    color: black !important;
}}

/* ===============================
   SIDEBAR (LIGHT – FIXED)
   =============================== */
section[data-testid="stSidebar"] {{
    background-color: #FFFFFF !important;
    border-right: 1px solid {CARD_BORDER};
}}

</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# UI HELPERS
# ============================================================

def render_section_title(title: str, icon: str = "📌"):
    st.markdown(f"<h2>{icon} {title}</h2>", unsafe_allow_html=True)
    st.markdown("---")


def render_kpi_cards(metrics: dict):
    cols = st.columns(len(metrics))
    for idx, (label, value) in enumerate(metrics.items()):
        with cols[idx]:
            st.markdown(
                f"""
<div class="sia-card">
    <div class="sia-card-title" style="font-size:2.1rem;">{value}</div>
    <div class="sia-card-desc">{label}</div>
</div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# BACK TO DASHBOARD
# ============================================================

def render_back_to_home():
    st.markdown(
        """
        <div style="
            position: fixed;
            top: 90px;
            right: 18px;
            z-index: 9999;
            background: rgba(255,255,255,0.95);
            padding: 10px 14px;
            border-radius: 999px;
            border: 1px solid rgba(0,0,0,0.1);
            box-shadow: 0 10px 28px rgba(0,0,0,0.14);
        ">
            🏠 <a href="./" target="_self"
                style="font-weight:800; color:#0E3A8A; text-decoration:none;">
                Back to Dashboard
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
