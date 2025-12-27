# ============================================================
# Author: Ruitao He & Qian Zhu
# Date: 2025-12
# Module 2: Customer Experience Analytics (Advanced Version)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from services.data_service import load_data
from services.ui_service import (
    apply_global_styles,
    inject_back_to_home_css,
    render_back_to_home,
)

sns.set(style="whitegrid")


# ============================================================
# Helpers
# ============================================================

def map_satisfaction(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["satisfaction"] = df["satisfaction"].astype(str).str.lower()

    mapping = {
        "very dissatisfied": 1,
        "dissatisfied": 2,
        "neutral or dissatisfied": 3,
        "neutral": 3,
        "neutral or satisfied": 4,
        "satisfied": 4,
        "very satisfied": 5,
    }

    df["satisfaction_score"] = df["satisfaction"].map(mapping).fillna(3)
    return df


def distance_bucket(km: float) -> str:
    if km < 1500:
        return "Short-haul"
    elif km < 3500:
        return "Medium-haul"
    return "Long-haul"


# ============================================================
# Streamlit UI
# ============================================================

def run_customer_experience_ui():

    st.set_page_config(
        page_title="Customer Experience Analytics",
        page_icon="😊",
        layout="wide",
    )

    # -------- Global UI & Navigation (CENTRALIZED) --------
    apply_global_styles()
    inject_back_to_home_css()
    render_back_to_home()

    # -----------------------------
    # Page Header
    # -----------------------------
    st.title("😊 Customer Experience Analytics")
    st.markdown(
        """
        This module provides **interactive customer experience analytics**.
        Users can dynamically segment passengers and explore how service
        attributes influence overall satisfaction.
        """
    )
    st.divider()

    # -----------------------------
    # Load & Prepare Data
    # -----------------------------
    df = load_data()
    if df is None or df.empty:
        st.error("❌ Dataset could not be loaded.")
        st.stop()

    df = map_satisfaction(df)
    df["Distance Segment"] = df["Flight Distance"].apply(distance_bucket)

    # -----------------------------
    # Sidebar Filters
    # -----------------------------
    st.sidebar.header("🎛 Customer Segmentation")

    cust_type = st.sidebar.multiselect(
        "Customer Type",
        options=sorted(df["Customer Type"].dropna().unique()),
        default=sorted(df["Customer Type"].dropna().unique()),
    )

    travel_class = st.sidebar.multiselect(
        "Class",
        options=sorted(df["Class"].dropna().unique()),
        default=sorted(df["Class"].dropna().unique()),
    )

    distance_seg = st.sidebar.multiselect(
        "Flight Distance",
        options=["Short-haul", "Medium-haul", "Long-haul"],
        default=["Short-haul", "Medium-haul", "Long-haul"],
    )

    filtered = df[
        df["Customer Type"].isin(cust_type)
        & df["Class"].isin(travel_class)
        & df["Distance Segment"].isin(distance_seg)
    ]

    # -----------------------------
    # KPI Summary
    # -----------------------------
    c1, c2, c3 = st.columns(3)
    c1.metric("Passengers", f"{len(filtered)}")
    c2.metric("Avg Satisfaction", f"{filtered['satisfaction_score'].mean():.2f}")
    c3.metric(
        "Satisfaction Rate (%)",
        f"{(filtered['satisfaction_score'] >= 4).mean() * 100:.1f}",
    )

    st.divider()

    # -----------------------------
    # Satisfaction Distribution
    # -----------------------------
    st.subheader("📊 Satisfaction Distribution")

    fig1, ax1 = plt.subplots()
    sns.countplot(
        x="satisfaction_score",
        data=filtered,
        ax=ax1,
    )
    ax1.set_xlabel("Satisfaction Score (1–5)")
    ax1.set_ylabel("Passengers")

    st.pyplot(fig1)
    st.divider()

    # -----------------------------
    # Segment Comparison
    # -----------------------------
    st.subheader("🧭 Satisfaction by Segment")

    seg_col = st.selectbox(
        "Compare by",
        ["Customer Type", "Class", "Distance Segment"],
    )

    fig2, ax2 = plt.subplots()
    filtered.groupby(seg_col)["satisfaction_score"].mean().plot(
        kind="bar",
        ax=ax2,
    )
    ax2.set_ylabel("Average Satisfaction")

    st.pyplot(fig2)
    st.divider()

    # -----------------------------
    # Driver Analysis
    # -----------------------------
    st.subheader("🔥 Key Satisfaction Drivers")

    service_cols = [
        "Seat comfort",
        "Inflight entertainment",
        "Food and drink",
        "On-board service",
        "Cleanliness",
        "Inflight service",
        "Checkin service",
    ]

    available = [c for c in service_cols if c in filtered.columns]

    corr = (
        filtered[available + ["satisfaction_score"]]
        .corr()["satisfaction_score"]
        .drop("satisfaction_score")
        .sort_values()
    )

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    corr.plot(kind="barh", ax=ax3)
    ax3.set_xlabel("Correlation with Satisfaction")

    st.pyplot(fig3)


# ============================================================
# CLI (Lightweight)
# ============================================================

def run_customer_experience_cli():

    
    df = load_data()
    df = map_satisfaction(df)

    print("\n=======================================")
    print(" CUSTOMER EXPERIENCE ANALYTICS (CLI) ")
    print("=======================================\n")

    print(f"Passengers           : {len(df)}")
    print(f"Avg Satisfaction     : {df['satisfaction_score'].mean():.2f}")
    print(
        f"Satisfaction Rate %  : {(df['satisfaction_score'] >= 4).mean() * 100:.1f}"
    )

    print("\nℹ️  Note:")
    print("Detailed segmentation and driver analysis")
    print("are available in the Streamlit UI.")

    input("\nPress ENTER to return to main menu...")


# ============================================================
# Auto-run Streamlit
# ============================================================

try:
    if st.runtime.exists():
        run_customer_experience_ui()
except Exception:
    pass
