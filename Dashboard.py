# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# ============================================

import sys
import logging

logging.basicConfig(level=logging.INFO)


# ============================================================
# STREAMLIT DASHBOARD (UI)
# ============================================================

def run_streamlit_ui():
    import base64
    from pathlib import Path

    import streamlit as st
    import streamlit.components.v1 as components
    from services.ui_service import apply_global_styles

    # -----------------------------
    # Page config
    # -----------------------------
    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="🏠",
        layout="wide"
    )

    apply_global_styles()

    # -----------------------------
    # Helpers
    # -----------------------------
    @st.cache_data(show_spinner=False)
    def file_to_base64(path: str) -> str | None:
        p = Path(path)
        if not p.exists():
            return None
        return base64.b64encode(p.read_bytes()).decode("utf-8")

    video_b64 = file_to_base64("assets/hero.mp4")
    logo_b64 = file_to_base64("assets/singapore_airlines_logo.png")

    # -----------------------------
    # HERO SECTION (STABLE VERSION)
    # -----------------------------
    logo_html = ""
    if logo_b64:
        logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}"
             style="
                height:72px;
                width:auto;
                border-radius:12px;
                background:rgba(255,255,255,0.92);
                padding:10px 14px;
             " />
        """

    if video_b64:
        hero_html = f"""
        <div style="
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            height: 420px;
            box-shadow: 0 14px 40px rgba(0,0,0,0.25);
            margin-bottom: 2.6rem;
        ">

            <video autoplay muted loop playsinline
                style="
                    position:absolute;
                    inset:0;
                    width:100%;
                    height:100%;
                    object-fit:cover;
                ">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>

            <div style="
                position:absolute;
                inset:0;
                background: linear-gradient(135deg,
                    rgba(0,26,77,0.88) 0%,
                    rgba(0,58,128,0.76) 55%,
                    rgba(0,26,77,0.82) 100%);
            "></div>

            <div style="
                position:relative;
                height:100%;
                padding:2.6rem 2.8rem;
                display:flex;
                flex-direction:column;
                justify-content:center;
                gap:0.9rem;
            ">
                <div style="display:flex; align-items:center; gap:14px;">
                    {logo_html}
                </div>

                <div style="
                    font-size:3.1rem;
                    font-weight:900;
                    letter-spacing:-1px;
                    color:#FFFFFF;
                    line-height:1.05;
                ">
                    Singapore Airlines Analytics System
                </div>

                <div style="
                    color:rgba(255,255,255,0.9);
                    font-size:1.15rem;
                    max-width:960px;
                ">
                    Enterprise cloud-based analytics dashboard for operational performance,
                    customer experience, risk scenarios, and cloud processing concepts.
                </div>
            </div>
        </div>
        """

        # ⚠️ height 一定要 >= 500，否则会被裁剪
        components.html(hero_html, height=520)

        st.caption("🎧 Optional: Click below to play the background media with sound.")
        st.video(f"data:video/mp4;base64,{video_b64}")

    else:
        st.warning("Hero video not found (assets/hero.mp4).")

    # -----------------------------
    # MODULE NAVIGATION
    # -----------------------------
    st.markdown("<h2>📊 Analytics Modules</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def module_card(title: str, desc: str, page_path: str):
        clicked = st.button(
            title,
            key=page_path,
            use_container_width=True,
        )

        st.markdown(
            f"""
            <div class="sia-card" style="margin-top:-58px; pointer-events:none;">
                <div class="sia-card-title">{title}</div>
                <div class="sia-card-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if clicked:
            st.switch_page(page_path)

    with col1:
        module_card(
            "✈️ Flight Performance Analytics",
            "Flight distance distribution, delay patterns, crew service indicators, and estimated fuel usage.",
            "pages/Module1_Flight_Performance.py",
        )
        module_card(
            "⚠️ Risk & Scenario Simulation",
            "Operational uncertainty modelling using simulation and disruption scenarios.",
            "pages/Module3_Risk_Simulation.py",
        )

    with col2:
        module_card(
            "😊 Customer Experience Analytics",
            "Passenger satisfaction, service ratings, and experience insights.",
            "pages/Module2_Customer_Experience.py",
        )
        module_card(
            "☁️ Cloud Analytics",
            "Batch vs streaming concepts and scalable processing demonstrations.",
            "pages/Module4_Cloud_Analytics.py",
        )

    st.info("Use the sidebar or click a module card to navigate.")


# ============================================================
# CLI DASHBOARD
# ============================================================

def run_cli():
    from pages.Module1_Flight_Performance import run_flight_performance_cli
    from pages.Module2_Customer_Experience import run_customer_experience_cli
    from pages.Module3_Risk_Simulation import run_cli as run_risk_simulation_cli
    from pages.Module4_Cloud_Analytics import run_cli as run_cloud_analytics_cli

    print("===========================================")
    print("   Singapore Airlines Analytics System CLI")
    print("===========================================")

    while True:
        print("\n1. Flight Performance Analytics")
        print("2. Customer Experience Analytics")
        print("3. Risk & Scenario Simulation")
        print("4. Cloud Analytics")
        print("5. Exit\n")

        choice = input("Enter option (1–5): ").strip()

        if choice == "1":
            run_flight_performance_cli()
        elif choice == "2":
            run_customer_experience_cli()
        elif choice == "3":
            run_risk_simulation_cli()
        elif choice == "4":
            run_cloud_analytics_cli()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("❌ Invalid option.")
            input("Press ENTER to continue...")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
