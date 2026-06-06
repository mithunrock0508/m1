import streamlit as st
import pandas as pd
import plotly.express as px

from analyzer import vehicle_analysis, adas_analysis

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Vehicle Telemetry & ADAS Analyzer",
    layout="wide"
)

st.title("🚗 Vehicle Telemetry & ADAS Analyzer")

st.markdown(
    "Upload Vehicle Telemetry CSV and ADAS CSV to analyze data."
)

# --------------------------------------------------
# CACHE FUNCTION
# --------------------------------------------------

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

# --------------------------------------------------
# FILE UPLOADS
# --------------------------------------------------

telemetry_file = st.file_uploader(
    "📁 Upload Vehicle Telemetry CSV",
    type=["csv"],
    key="telemetry"
)

adas_file = st.file_uploader(
    "📁 Upload ADAS CSV",
    type=["csv"],
    key="adas"
)

# --------------------------------------------------
# LOAD FILES ONLY ONCE
# --------------------------------------------------

telemetry_df = None
adas_df = None

try:
    if telemetry_file is not None:
        telemetry_df = load_csv(telemetry_file)

    if adas_file is not None:
        adas_df = load_csv(adas_file)

except Exception as e:
    st.error(f"Error loading file: {e}")

# ==================================================
# VEHICLE TELEMETRY DASHBOARD
# ==================================================

if telemetry_df is not None:

    st.divider()
    st.header("🚗 Vehicle Telemetry Dashboard")

    st.subheader("Dataset Preview")
    st.dataframe(telemetry_df.head())

    st.write(f"Rows: {telemetry_df.shape[0]}")
    st.write(f"Columns: {telemetry_df.shape[1]}")

    try:

        results = vehicle_analysis(telemetry_df)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Average Speed",
            f"{results['avg_speed']:.2f} km/h"
        )

        c2.metric(
            "Maximum Speed",
            f"{results['max_speed']:.2f} km/h"
        )

        c3.metric(
            "Average Fuel",
            f"{results['avg_fuel']:.2f}%"
        )

        c4.metric(
            "Average Engine Temp",
            f"{results['avg_temp']:.2f} °C"
        )

        # Speed Distribution
        if "speed_kmh" in telemetry_df.columns:

            st.subheader("Speed Distribution")

            fig = px.histogram(
                telemetry_df,
                x="speed_kmh",
                nbins=25
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # Fuel Trend
        if "fuel_level_pct" in telemetry_df.columns:

            st.subheader("Fuel Level Trend")

            fig2 = px.line(
                telemetry_df.head(1000),
                y="fuel_level_pct"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        # Status Codes
        if "status_code" in telemetry_df.columns:

            st.subheader("Vehicle Status Distribution")

            st.bar_chart(
                telemetry_df["status_code"].value_counts()
            )

    except Exception as e:
        st.error(f"Telemetry Analysis Error: {e}")

# ==================================================
# ADAS DASHBOARD
# ==================================================

if adas_df is not None:

    st.divider()
    st.header("🤖 ADAS Dashboard")

    st.subheader("Dataset Preview")

    st.dataframe(adas_df.head())

    st.write(f"Rows: {adas_df.shape[0]}")
    st.write(f"Columns: {adas_df.shape[1]}")

    try:

        results = adas_analysis(adas_df)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Average Speed",
            f"{results['avg_speed']:.2f} km/h"
        )

        c2.metric(
            "Battery Level",
            f"{results['battery']:.2f}%"
        )

        c3.metric(
            "Energy Consumption",
            f"{results['energy']:.2f}"
        )

        c4.metric(
            "Reaction Time",
            f"{results['reaction']:.2f} sec"
        )

        # ADAS Output
        if "ADAS_output" in adas_df.columns:

            st.subheader("ADAS Decisions")

            st.bar_chart(
                adas_df["ADAS_output"].value_counts()
            )

        # Battery Trend
        if "battery_level" in adas_df.columns:

            st.subheader("Battery Trend")

            fig3 = px.line(
                adas_df.head(1000),
                y="battery_level"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        # Obstacle Distance
        if (
            "speed_kmh" in adas_df.columns and
            "obstacle_distance" in adas_df.columns and
            "ADAS_output" in adas_df.columns
        ):

            st.subheader("Obstacle Distance vs Speed")

            fig4 = px.scatter(
                adas_df,
                x="speed_kmh",
                y="obstacle_distance",
                color="ADAS_output"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

    except Exception as e:
        st.error(f"ADAS Analysis Error: {e}")

# ==================================================
# COMBINED INSIGHTS
# ==================================================

if telemetry_df is not None and adas_df is not None:

    st.divider()
    st.header("📊 Combined Insights")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Telemetry Records",
        len(telemetry_df)
    )

    c2.metric(
        "ADAS Records",
        len(adas_df)
    )

    c3.metric(
        "Total Records",
        len(telemetry_df) + len(adas_df)
    )

    # Combined Speed Comparison

    if (
        "speed_kmh" in telemetry_df.columns and
        "speed_kmh" in adas_df.columns
    ):

        st.subheader("Average Speed Comparison")

        comparison_df = pd.DataFrame({
            "Dataset": ["Telemetry", "ADAS"],
            "Average Speed": [
                telemetry_df["speed_kmh"].mean(),
                adas_df["speed_kmh"].mean()
            ]
        })

        fig5 = px.bar(
            comparison_df,
            x="Dataset",
            y="Average Speed"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )
