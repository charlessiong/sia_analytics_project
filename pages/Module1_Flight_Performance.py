# ============================================================
# Author: Charles
# Date: 2025-12
# Description:
# Module 1 – Flight Performance Analytics
#
# This module provides:
# - Streamlit UI for visual analytics
# - CLI mode for summary-based analytics
#
# Fuel consumption is synthetically estimated based on
# flight distance due to the absence of real fuel data.
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from services.data_service import load_data


# ============================================================
# SHARED LOGIC — DATA PREPARATION
# ============================================================

def prepare_flight_data():
    """
    Load dataset and simulate fuel consumption.
    Shared by both UI and CLI to ensure consistency.
    """
    df = load_data()

    if df is None or df.empty:
        return None

    # Simulate fuel consumption (academic estimation)
    BASE_FUEL_RATE = 0.05  # kg per km
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
    total_flights = len(df)
    avg_distance = df["Flight Distance"].mean()
    avg_dep_delay = df["Departure Delay in Minutes"].mean()
    avg_arr_delay = df["Arrival Delay in Minutes"].mean()
    avg_fuel = df["Estimated Fuel Consumption (kg)"].mean()

    render_kpi_cards(
        {
            "Total Flights": total_flights,
            "Avg Distance (km)": f"{avg_distance:.1f}",
            "Avg Fuel (kg)": f"{avg_fuel:.1f}",
            "Avg Arrival Delay (min)": f"{avg_arr_delay:.1f}",
        }
    )

    st.divider()

    # -------------------------------
    # FLIGHT DISTANCE DISTRIBUTION
    # -------------------------------
    st.subheader("📈 Flight Distance Distribution")

    fig1, ax1 = plt.subplots()
    ax1.hist(df["Flight Distance"], bins=30)
    ax1.set_xlabel("Flight Distance (km)")
    ax1.set_ylabel("Number of Flights")

    st.pyplot(fig1)
    st.divider()

    # -------------------------------
    # DELAY ANALYSIS
    # -------------------------------
    st.subheader("⏱ Arrival Delay vs Flight Distance")

    fig2, ax2 = plt.subplots()
    ax2.scatter(
        df["Flight Distance"],
        df["Arrival Delay in Minutes"],
        alpha=0.3
    )
    ax2.set_xlabel("Flight Distance (km)")
    ax2.set_ylabel("Arrival Delay (minutes)")

    st.pyplot(fig2)
    st.divider()

    # -------------------------------
    # FUEL CONSUMPTION ANALYSIS
    # -------------------------------
    st.subheader("⛽ Estimated Fuel Consumption vs Flight Distance")

    fig3, ax3 = plt.subplots()
    ax3.scatter(
        df["Flight Distance"],
        df["Estimated Fuel Consumption (kg)"],
        alpha=0.4
    )
    ax3.set_xlabel("Flight Distance (km)")
    ax3.set_ylabel("Estimated Fuel Consumption (kg)")

    st.pyplot(fig3)
    st.divider()

    # -------------------------------
    # CREW PERFORMANCE
    # -------------------------------
    st.subheader("👨‍✈️ Crew Service Performance")

    crew_cols = [
        "On-board service",
        "Inflight service",
        "Checkin service",
    ]

    available = [c for c in crew_cols if c in df.columns]

    if available:
        crew_avg = df[available].mean().sort_values()

        fig4, ax4 = plt.subplots()
        crew_avg.plot(kind="barh", ax=ax4)
        ax4.set_xlabel("Average Rating (1–5)")

        st.pyplot(fig4)
    else:
        st.warning("Crew service columns not found in dataset.")

    st.divider()

    st.page_link("Dashboard.py", label="⬅️ Back to Dashboard", icon="🏠")


# ============================================================
# CLI VERSION
# ============================================================

def run_flight_performance_cli():
    """
    Command-line interface for Flight Performance Analytics.
    Provides summary statistics without visualizations.
    """

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

    crew_cols = [
        "On-board service",
        "Inflight service",
        "Checkin service",
    ]

    available = [c for c in crew_cols if c in df.columns]

    if available:
        print("\n👨‍✈️ Crew Service Ratings:")
        for col in available:
            print(f" - {col}: {df[col].mean():.2f}")

    print("\n✔ Flight Performance CLI completed.")
    input("\nPress ENTER to return to main menu...")


# ============================================================
# AUTO-RUN STREAMLIT WHEN OPENED AS PAGE
# ============================================================

try:
    import streamlit as st
    if st.runtime.exists():
        run_flight_performance_ui()
except Exception:
    pass
