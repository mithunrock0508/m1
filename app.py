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

st.title("🚗 Vehicle Mileage & ADAS Telemetry Analyzer")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.write("Rows:", df.shape[0])
    st.write("Columns:", df.shape[1])

    st.divider()

    # Vehicle Telemetry Dataset
    if "vehicle_id" in df.columns:

        st.header("Vehicle Telemetry Analysis")

        results = vehicle_analysis(df)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Average Speed",
            f"{results['avg_speed']:.2f} km/h"
        )

        c2.metric(
            "Max Speed",
            f"{results['max_speed']:.2f} km/h"
        )

        c3.metric(
            "Average Fuel",
            f"{results['avg_fuel']:.2f}%"
        )

        c4.metric(
            "Average Engine Temp",
            f"{results['avg_temp']:.2f}°C"
        )

        st.subheader("Speed Distribution")

        fig = px.histogram(
            df,
            x="speed_kmh",
            nbins=30
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Fuel Level")

        fig2 = px.line(
            df.head(500),
            y="fuel_level_pct"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Vehicle Status")

        st.bar_chart(
            df["status_code"].value_counts()
        )

    # ADAS Dataset
    elif "ADAS_output" in df.columns:

        st.header("ADAS Analysis")

        results = adas_analysis(df)

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
            f"{results['reaction']:.2f}s"
        )

        st.subheader("ADAS Decisions")

        st.bar_chart(
            df["ADAS_output"].value_counts()
        )

        st.subheader("Battery Level")

        fig3 = px.line(
            df.head(1000),
            y="battery_level"
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Obstacle Distance")

        fig4 = px.scatter(
            df,
            x="speed_kmh",
            y="obstacle_distance",
            color="ADAS_output"
        )

        st.plotly_chart(fig4, use_container_width=True)

    else:
        st.error(
            "Unknown dataset format."
        )
