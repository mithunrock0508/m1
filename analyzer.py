def vehicle_analysis(df):

    return {
        "avg_speed": df["speed_kmh"].mean(),
        "max_speed": df["speed_kmh"].max(),
        "avg_fuel": df["fuel_level_pct"].mean(),
        "avg_temp": df["engine_temp_c"].mean()
    }


def adas_analysis(df):

    return {
        "avg_speed": df["speed_kmh"].mean(),
        "battery": df["battery_level"].mean(),
        "energy": df["energy_consumption"].mean(),
        "reaction": df["reaction_time"].mean()
    }
