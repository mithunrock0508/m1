import streamlit as st
import pandas as pd
import plotly.express as px

from analyzer import (
    vehicle_analysis,
    adas_analysis
)

st.set_page_config(
    page_title="Vehicle Telemetry & ADAS Analyzer",
    layout="wide"
)

st.title("🚗 Vehicle Telemetry & ADAS Analyzer")

# ==========================
# Upload Section
# ==========================

telemetry_file = st.file_uploader(
    "Upload Vehicle Telemetry CSV",
    type=["csv"],
    key="telemetry"
)

adas_file = st.file_uploader(
    "Upload ADAS CSV",
    type=["csv"],
    key="adas"
)

# ==========================
# TELEMETRY DASHBOARD
# ==========================

if telemetry_file:

    st.header("🚗 Vehicle Telemetry Dashboard")

    telemetry_df = pd.read_csv(telemetry_file)

    st.dataframe(telemetry_df.head())

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
        "Fuel Level",
        f"{results['avg_fuel']:.2f}%"
    )

    c4.metric(
        "Engine Temp",
        f"{results['avg_temp']:.2f} °C"
    )

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

    st.subheader("Fuel Trend")

    fig2 = px.line(
        telemetry_df.head(1000),
        y="fuel_level_pct"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================
# ADAS DASHBOARD
# ==========================

if adas_file:

    st.header("🤖 ADAS Dashboard")

    adas_df = pd.read_csv(adas_file)

    st.dataframe(adas_df.head())

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

    st.subheader("ADAS Output")

    st.bar_chart(
        adas_df["ADAS_output"].value_counts()
    )

    st.subheader("Battery Trend")

    fig3 = px.line(
        adas_df.head(1000),
        y="battery_level"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

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

# ==========================
# BOTH FILES UPLOADED
# ==========================

if telemetry_file and adas_file:

    st.header("📊 Combined Insights")

    telemetry_df = pd.read_csv(telemetry_file)
    adas_df = pd.read_csv(adas_file)

    st.write(
        f"Telemetry Records: {len(telemetry_df)}"
    )

    st.write(
        f"ADAS Records: {len(adas_df)}"
    )

    st.metric(
        "Combined Records",
        len(telemetry_df) + len(adas_df)
    )
