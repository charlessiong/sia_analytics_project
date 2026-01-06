# ============================================================
# ui_service.py – Singapore Airlines Inspired Global UI Theme
# ============================================================

import streamlit as st

# ============================================================
# SIA Color Palette
# ============================================================

PRIMARY_NAVY = "#002663"
ACCENT_GOLD = "#FFED4D"
BACKGROUND_CREAM = "#F5F3EE"
TEXT_GREY = "#555555"

CARD_BG = "#FFFFFF"
CARD_BORDER = "#E5E7EB"


# ============================================================
# GLOBAL STYLE INJECTION
# ============================================================

def apply_global_styles():
    st.markdown(
        f"""
<style>

/* ===============================
   Global App Background
   =============================== */
.stApp {{
    background-color: {BACKGROUND_CREAM} !important;
}}

/* ===============================
   Main Content Padding
   =============================== */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}}

/* ===============================
   Headings
   =============================== */
h1, h2, h3 {{
    color: {PRIMARY_NAVY} !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
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
   SIA CARD (⭐ FINAL VERSION ⭐)
   =============================== */
.sia-card {{
    background: {CARD_BG};
    padding: 1.4rem 1.6rem;
    border-radius: 16px;
    border: 1px solid {CARD_BORDER};
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);

    /* ⭐ KEY FIX: force equal height */
    min-height: 210px;

    /* Clean layout */
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    transition: 0.2s ease-in-out;
}}

.sia-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.12);
    cursor: pointer;
}}

/* ===============================
   Card Title
   =============================== */
.sia-card-title {{
    color: {PRIMARY_NAVY};
    font-size: 1.4rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}}

/* ===============================
   Card Description
   =============================== */
.sia-card-desc {{
    color: {TEXT_GREY};
    font-size: 1rem;
    line-height: 1.45;
}}

/* ===============================
   KPI Metric
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
   Sidebar
   =============================== */
section[data-testid="stSidebar"] {
    background-color: {PRIMARY_NAVY} !important;
    border-right: 1px solid {CARD_BORDER};
}}


/* ===============================
   KPI Cards (Module 3 / 4)
   =============================== */

.kpi-card {{
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}}

.kpi-title {{
    color: #555555;         
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 6px;
}}

.kpi-value {{
    color: #002663;              /* SIA Navy */
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.1;
}}

.kpi-badge {{
    display: inline-block;
    margin-top: 8px;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(255, 237, 77, 0.35);
    color: #002663;
    font-weight: 700;
    font-size: 0.78rem;
}}

</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# UI HELPER COMPONENTS
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
# GLOBAL NAVIGATION – Back to Dashboard
# ============================================================

def inject_back_to_home_css():
    """
    Inject shared CSS for Back-to-Dashboard links.
    Used by all modules for consistent navigation UX.
    """
    st.markdown(
        f"""
<style>
/* ===============================
   Back to Dashboard (Top Row)
   =============================== */
.back-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 6px 0 14px 0;
    font-size: 1rem;
}}

.back-row a {{
    text-decoration: none;
    font-weight: 700;
    color: {PRIMARY_NAVY};
}}

.back-row a:hover {{
    text-decoration: underline;
}}

/* ===============================
   Floating Back Button
   =============================== */
.sia-back-float {{
    position: fixed;
    top: 90px;
    right: 18px;
    z-index: 999999;

    display: inline-flex;
    align-items: center;
    gap: 10px;

    padding: 10px 14px;
    border-radius: 999px;

    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(0,0,0,0.10);
    box-shadow: 0 10px 28px rgba(0,0,0,0.14);

    backdrop-filter: blur(6px);
}}

.sia-back-float a {{
    text-decoration: none;
    font-weight: 800;
    color: {PRIMARY_NAVY};
    font-size: 0.98rem;
}}

.sia-back-float a:hover {{
    text-decoration: underline;
}}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_back_to_home():
    """
    Render both:
    - top inline back link
    - floating back button
    """

    st.markdown(
        """
        <div class="sia-back-float">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chart(fig, use_full_width=False):
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True, use_container_width=use_full_width)
