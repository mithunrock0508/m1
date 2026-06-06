# ==================================================
# ADVANCED VEHICLE INTELLIGENCE
# ==================================================

import numpy as np
from sklearn.ensemble import IsolationForest

if telemetry_df is not None:

    st.divider()
    st.header("🚀 Vehicle Intelligence Center")

    # ----------------------------
    # Vehicle Health Score
    # ----------------------------

    avg_speed = telemetry_df["speed_kmh"].mean()
    avg_fuel = telemetry_df["fuel_level_pct"].mean()
    avg_temp = telemetry_df["engine_temp_c"].mean()

    vehicle_health = max(
        0,
        min(100, 100 - ((avg_temp - 75) * 2))
    )

    eco_score = 100

    if avg_speed > 80:
        eco_score -= 20

    if avg_temp > 95:
        eco_score -= 20

    if avg_fuel < 30:
        eco_score -= 20

    eco_score = max(eco_score, 0)

    # ----------------------------
    # Driver Profile
    # ----------------------------

    if avg_speed > 90:
        driver_type = "🔥 Aggressive Driver"

    elif avg_speed > 60:
        driver_type = "🚗 Normal Driver"

    else:
        driver_type = "🌱 Eco Driver"

    # ----------------------------
    # KPI CARDS
    # ----------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "❤️ Vehicle Health",
        f"{vehicle_health:.0f}/100"
    )

    c2.metric(
        "🌱 Eco Score",
        f"{eco_score}/100"
    )

    c3.metric(
        "🚗 Driver Profile",
        driver_type
    )

    # ----------------------------
    # Correlation Heatmap
    # ----------------------------

    st.subheader("📊 Vehicle Correlation Heatmap")

    numeric_df = telemetry_df.select_dtypes(
        include=["number"]
    )

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------
    # Anomaly Detection
    # ----------------------------

    st.subheader("🚨 AI Anomaly Detection")

    required_cols = [
        "speed_kmh",
        "engine_temp_c"
    ]

    if all(
        col in telemetry_df.columns
        for col in required_cols
    ):

        anomaly_df = telemetry_df[
            required_cols
        ].dropna()

        if len(anomaly_df) > 10:

            model = IsolationForest(
                contamination=0.05,
                random_state=42
            )

            anomaly_df["anomaly"] = (
                model.fit_predict(
                    anomaly_df
                )
            )

            anomaly_count = (
                anomaly_df["anomaly"] == -1
            ).sum()

            st.metric(
                "Detected Anomalies",
                anomaly_count
            )

            fig = px.scatter(
                anomaly_df,
                x="speed_kmh",
                y="engine_temp_c",
                color=anomaly_df[
                    "anomaly"
                ].astype(str),
                title="Vehicle Anomalies"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ----------------------------
    # Mileage Intelligence
    # ----------------------------

    st.subheader("⛽ Mileage Intelligence")

    mileage_loss = pd.DataFrame({
        "Factor": [
            "Overspeeding",
            "Engine Load",
            "High Temperature",
            "Driving Pattern"
        ],
        "Impact": [
            40,
            25,
            20,
            15
        ]
    })

    fig = px.bar(
        mileage_loss,
        x="Factor",
        y="Impact",
        color="Impact",
        title="Mileage Loss Contributors"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ----------------------------
    # AI Recommendations
    # ----------------------------

    st.subheader("🤖 AI Recommendations")

    recommendations = []

    if avg_speed > 80:
        recommendations.append(
            "Reduce average speed to improve mileage."
        )

    if avg_temp > 95:
        recommendations.append(
            "Engine temperature is high. Maintenance recommended."
        )

    if avg_fuel < 30:
        recommendations.append(
            "Fuel efficiency is decreasing."
        )

    if vehicle_health < 75:
        recommendations.append(
            "Vehicle health is below optimal range."
        )

    if not recommendations:
        recommendations.append(
            "Vehicle operating parameters are healthy."
        )

    for rec in recommendations:
        st.success(rec)
