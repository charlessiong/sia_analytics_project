# ============================================================
# Author: Charles
# Date: 2025-12
# Module 1 – Flight Performance Analytics
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from services.data_service import load_data
from services.ui_service import (
    apply_global_styles,
    inject_back_to_home_css,
    render_back_to_home,
)


# ============================================================
# SHARED LOGIC — DATA PREPARATION
# ============================================================

def prepare_flight_data():
    df = load_data()
    if df is None or df.empty:
        return None

    BASE_FUEL_RATE = 0.05
    np.random.seed(42)

    df["Estimated Fuel Consumption (kg)"] = (
        df["Flight Distance"]
        * BASE_FUEL_RATE
        * np.random.uniform(0.9, 1.1, size=len(df))
    )
    return df


# ============================================================
# STREAMLIT UI VERSION
# ============================================================

def run_flight_performance_ui():

    import streamlit as st
    from services.ui_service import apply_global_styles, render_kpi_cards

    st.set_page_config(
        page_title="Flight Performance Analytics",
        page_icon="✈️",
        layout="wide"
    )

    apply_global_styles()
    inject_back_to_home_css()
    render_back_to_home()


    # -------------------------------
    # PAGE HEADER
    # -------------------------------
    st.title("✈️ Flight Performance Analytics")
    st.markdown(
        """
        This module analyzes **operational flight performance**, including:

        - Flight distance characteristics  
        - Departure and arrival delays  
        - Crew service performance  
        - **Estimated fuel consumption (simulated)**  
        """
    )

    st.divider()

    # -------------------------------
    # LOAD & PREPARE DATA
    # -------------------------------
    df = prepare_flight_data()
    if df is None:
        st.error("❌ Unable to load dataset.")
        st.stop()

    # -------------------------------
    # KPI SECTION
    # -------------------------------
    render_kpi_cards(
        {
            "Total Flights": len(df),
            "Avg Distance (km)": f"{df['Flight Distance'].mean():.1f}",
            "Avg Fuel (kg)": f"{df['Estimated Fuel Consumption (kg)'].mean():.1f}",
            "Avg Arrival Delay (min)": f"{df['Arrival Delay in Minutes'].mean():.1f}",
        }
    )

    st.divider()

    # -------------------------------
    # VISUAL ANALYTICS
    # -------------------------------
    st.subheader("📈 Flight Distance Distribution")
    fig1, ax1 = plt.subplots()
    ax1.hist(df["Flight Distance"], bins=30)
    ax1.set_xlabel("Flight Distance (km)")
    ax1.set_ylabel("Number of Flights")
    st.pyplot(fig1)
    st.divider()

    st.subheader("⏱ Arrival Delay vs Flight Distance")
    fig2, ax2 = plt.subplots()
    ax2.scatter(df["Flight Distance"], df["Arrival Delay in Minutes"], alpha=0.3)
    ax2.set_xlabel("Flight Distance (km)")
    ax2.set_ylabel("Arrival Delay (minutes)")
    st.pyplot(fig2)
    st.divider()

    st.subheader("⛽ Estimated Fuel Consumption vs Flight Distance")
    fig3, ax3 = plt.subplots()
    ax3.scatter(df["Flight Distance"], df["Estimated Fuel Consumption (kg)"], alpha=0.4)
    ax3.set_xlabel("Flight Distance (km)")
    ax3.set_ylabel("Estimated Fuel Consumption (kg)")
    st.pyplot(fig3)
    st.divider()

    st.subheader("👨‍✈️ Crew Service Performance")
    crew_cols = ["On-board service", "Inflight service", "Checkin service"]
    available = [c for c in crew_cols if c in df.columns]

    if available:
        crew_avg = df[available].mean().sort_values()
        fig4, ax4 = plt.subplots()
        crew_avg.plot(kind="barh", ax=ax4)
        ax4.set_xlabel("Average Rating (1–5)")
        st.pyplot(fig4)
    else:
        st.warning("Crew service columns not found in dataset.")


# ============================================================
# CLI VERSION (UNCHANGED)
# ============================================================

def run_flight_performance_cli():
    print("\n=======================================")
    print("  FLIGHT PERFORMANCE ANALYTICS (CLI)   ")
    print("=======================================\n")

    df = prepare_flight_data()
    if df is None:
        print("❌ ERROR: Unable to load dataset.")
        input("Press ENTER to return...")
        return

    print(f"✈️ Total Flights        : {len(df)}")
    print(f"📏 Avg Distance (km)    : {df['Flight Distance'].mean():.1f}")
    print(f"⏱ Avg Departure Delay  : {df['Departure Delay in Minutes'].mean():.1f} min")
    print(f"🛬 Avg Arrival Delay    : {df['Arrival Delay in Minutes'].mean():.1f} min")
    print(f"⛽ Avg Fuel Consumption : {df['Estimated Fuel Consumption (kg)'].mean():.1f} kg")

    print("\n✔ Flight Performance CLI completed.")
    input("\nPress ENTER to return to main menu...")


# ============================================================
# AUTO-RENDER STREAMLIT PAGE
# ============================================================

try:
    import streamlit as st
    if st.runtime.exists():
        run_flight_performance_ui()
except Exception:
    pass
