import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Air Quality Forecaster", layout="wide")

st.markdown("""
<style>
.title    { text-align: center; font-size: 38px; font-weight: bold; }
.subtitle { text-align: center; color: #9aa0a6; margin-bottom: 20px; }
.stButton>button {
    background-color: #1f6feb; color: white;
    border-radius: 8px; padding: 8px 20px; width: 100%;
}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_assets():
    return {
        "models": {
            "t1":  joblib.load("air_quality_model_t1.pkl"),
            "t6":  joblib.load("air_quality_model_t6.pkl"),
            "t24": joblib.load("air_quality_model_t24.pkl"),
        },
        "season":   joblib.load("season_encoding.pkl"),
        "wind":     joblib.load("wind_direction_encoding.pkl"),
        "features": joblib.load("features.pkl"),
    }


assets = load_assets()


# --- EPA piecewise linear AQI formula ---
def pm25_to_aqi(pm):
    breakpoints = [
        (0.0,    12.0,   0,  50),
        (12.1,   35.4,  51, 100),
        (35.5,   55.4, 101, 150),
        (55.5,  150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ]
    for bp_lo, bp_hi, aqi_lo, aqi_hi in breakpoints:
        if bp_lo <= pm <= bp_hi:
            return round(((aqi_hi - aqi_lo) / (bp_hi - bp_lo)) * (pm - bp_lo) + aqi_lo)
    return 500


def aqi_category(aqi):
    if aqi <= 50:    return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy for Sensitive Groups"
    elif aqi <= 200: return "Unhealthy"
    elif aqi <= 300: return "Very Unhealthy"
    else:            return "Hazardous"


AQI_COLOR = {
    "Good":                           "#00e400",
    "Moderate":                       "#ffff00",
    "Unhealthy for Sensitive Groups": "#ff7e00",
    "Unhealthy":                      "#ff0000",
    "Very Unhealthy":                 "#8f3f97",
    "Hazardous":                      "#7e0023",
}

ADVISORY = {
    "Good": {
        "General Public":    "Air quality is satisfactory. No restrictions on outdoor activity.",
        "Elderly":           "No restrictions. Enjoy outdoor activities.",
        "Children":          "No restrictions. Outdoor play is safe.",
        "Respiratory":       "No restrictions.",
        "Cardiovascular":    "No restrictions.",
    },
    "Moderate": {
        "General Public":    "Unusually sensitive individuals may experience minor effects.",
        "Elderly":           "Limit prolonged outdoor exertion if you feel discomfort.",
        "Children":          "Reduce extended outdoor play if child shows sensitivity.",
        "Respiratory":       "Keep rescue inhaler accessible during outdoor activities.",
        "Cardiovascular":    "Monitor symptoms during physical activity outdoors.",
    },
    "Unhealthy for Sensitive Groups": {
        "General Public":    "General public unlikely to be affected. Sensitive groups at risk.",
        "Elderly":           "Avoid prolonged outdoor exertion. Stay indoors when possible.",
        "Children":          "Reduce outdoor playtime. Avoid high-exertion activities.",
        "Respiratory":       "Avoid outdoor exertion. Use prescribed medication as directed.",
        "Cardiovascular":    "Avoid strenuous outdoor activity. Monitor heart rate.",
    },
    "Unhealthy": {
        "General Public":    "Everyone should reduce prolonged outdoor exertion.",
        "Elderly":           "Stay indoors. Wear N95 mask if going outside.",
        "Children":          "No outdoor activities. Keep windows closed.",
        "Respiratory":       "Stay indoors. Use air purifier. Have emergency medication ready.",
        "Cardiovascular":    "Stay indoors. Avoid all physical exertion.",
    },
    "Very Unhealthy": {
        "General Public":    "Avoid all outdoor exertion. Move activities indoors.",
        "Elderly":           "Do not go outside. Seek medical attention if symptoms develop.",
        "Children":          "Keep indoors. Seal gaps in windows and doors.",
        "Respiratory":       "Stay indoors, use inhaler, call doctor if symptoms worsen.",
        "Cardiovascular":    "Stay indoors, avoid all exertion, seek medical help immediately.",
    },
    "Hazardous": {
        "General Public":    "Health emergency. Everyone should avoid all outdoor activities.",
        "Elderly":           "Do not leave home. Call emergency services if feeling unwell.",
        "Children":          "Do not leave home. Use air purifier indoors.",
        "Respiratory":       "Critical — stay indoors, use nebulizer/inhaler, call emergency if needed.",
        "Cardiovascular":    "Critical — stay indoors, complete rest, seek emergency care immediately.",
    },
}


# --- UI ---
st.markdown('<div class="title">🌍 Air Quality Forecaster</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Forecast PM2.5 & AQI up to 24 hours ahead · '
    'Population-specific health advisory</div>',
    unsafe_allow_html=True,
)
st.divider()

col1, col_mid, col2 = st.columns([1, 0.05, 1])
now = datetime.now()

with col1:
    st.subheader("Input Parameters")

    st.markdown("**Current Readings**")
    current_pm25 = st.number_input("Current PM2.5 (µg/m³)", min_value=0.0, max_value=999.0, value=35.0)
    temperature  = st.number_input("Temperature (°C)", min_value=-40.0, max_value=60.0, value=20.0)
    pressure     = st.number_input("Pressure (hPa)", min_value=900.0, max_value=1100.0, value=1013.0)
    wind_speed   = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=50.0, value=3.0)
    wind_dir     = st.selectbox("Wind Direction", sorted(assets["wind"].keys()))
    season       = st.selectbox("Season", sorted(assets["season"].keys()))

    st.markdown("**Time**")
    hour      = st.slider("Hour of Day", 0, 23, now.hour)
    day       = st.slider("Day of Month", 1, 31, now.day)
    month     = st.slider("Month", 1, 12, now.month)
    dayofweek = now.weekday()

    with st.expander("Advanced Pollutant Inputs"):
        pm10          = st.number_input("PM10 (µg/m³)",         min_value=0.0, value=50.0)
        so2           = st.number_input("SO2 (µg/m³)",          min_value=0.0, value=15.0)
        no2           = st.number_input("NO2 (µg/m³)",          min_value=0.0, value=30.0)
        co            = st.number_input("CO (µg/m³)",           min_value=0.0, value=500.0)
        o3            = st.number_input("O3 (µg/m³)",           min_value=0.0, value=40.0)
        dew_point     = st.number_input("Dew Point (°C)",       value=temperature - 10.0)
        precipitation = st.number_input("Precipitation (mm/h)", min_value=0.0, value=0.0)

    st.markdown("**Forecast Settings**")
    horizon_label = st.selectbox(
        "Forecast Horizon",
        ["1 hour ahead", "6 hours ahead", "24 hours ahead"],
    )
    horizon_key = {"1 hour ahead": "t1", "6 hours ahead": "t6", "24 hours ahead": "t24"}
    horizon     = horizon_key[horizon_label]

    population = st.selectbox(
        "Population Group",
        ["General Public", "Elderly", "Children", "Respiratory", "Cardiovascular"],
    )

    predict_btn = st.button("Forecast Air Quality", use_container_width=True)

with col_mid:
    st.markdown(
        '<div style="border-left:2px solid #2c2f36;height:900px;margin:auto;"></div>',
        unsafe_allow_html=True,
    )

with col2:
    st.subheader("Forecast Results")

    if predict_btn:
        with st.spinner("Running forecast..."):
            input_data = {
                "Season":                       assets["season"].get(season, 0),
                "PM10 concentration (ug/m^3)":  pm10,
                "SO2 concentration (ug/m^3)":   so2,
                "NO2 concentration (ug/m^3)":   no2,
                "CO concentration (ug/m^3)":    co,
                "O3 concentration (ug/m^3)":    o3,
                "Pressure (hPa)":               pressure,
                "Wind Direction":               assets["wind"].get(wind_dir, 0),
                "Wind Speed (m/s)":             wind_speed,
                "Precipitation (mm, hourly)":   precipitation,
                "Dew Point (Celsius)":          dew_point,
                "Temperature (Celsius)":        temperature,
                "hour":                         hour,
                "day":                          day,
                "month":                        month,
                "dayofweek":                    dayofweek,
                "PM2.5_lag1":                   current_pm25,
                "PM2.5_lag3":                   current_pm25,
                "PM2.5_rolling6h":              current_pm25,
                "PM2.5_rolling24h":             current_pm25,
            }
            input_df  = pd.DataFrame([input_data]).reindex(columns=assets["features"])
            pred_pm25 = max(0.0, assets["models"][horizon].predict(input_df)[0])
            pred_aqi  = pm25_to_aqi(pred_pm25)
            category  = aqi_category(pred_aqi)
            color     = AQI_COLOR[category]
            advisory  = ADVISORY[category][population]

        # Current vs forecast metrics
        curr_aqi = pm25_to_aqi(current_pm25)
        curr_cat = aqi_category(curr_aqi)

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Current AQI", curr_aqi)
            st.caption(f"Category: {curr_cat}")
        with c2:
            st.metric(
                f"Forecast ({horizon_label})",
                pred_aqi,
                delta=pred_aqi - curr_aqi,
                delta_color="inverse",
            )
            st.caption(f"Category: {category}")

        st.markdown(f"""
        <div style='background:{color}22;border-left:4px solid {color};
                    padding:12px;border-radius:6px;margin:12px 0;'>
            <b style='color:{color};font-size:16px;'>{category}</b><br>
            PM2.5 forecast: <b>{pred_pm25:.1f} µg/m³</b> &nbsp;·&nbsp; AQI: <b>{pred_aqi}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Health Advisory")
        st.markdown(f"**Group:** {population}")
        st.info(advisory)

        # All 3 horizons comparison table
        st.markdown("### All Horizons")
        rows = []
        for h, label in [("t1", "1h"), ("t6", "6h"), ("t24", "24h")]:
            p_pm  = max(0.0, assets["models"][h].predict(input_df)[0])
            p_aqi = pm25_to_aqi(p_pm)
            p_cat = aqi_category(p_aqi)
            rows.append({
                "Horizon":       f"+{label}",
                "PM2.5 (µg/m³)": round(p_pm, 1),
                "AQI":           p_aqi,
                "Category":      p_cat,
                "Advisory":      ADVISORY[p_cat][population][:65] + "...",
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    else:
        st.markdown("""
        <div style='background:#1f2a38;padding:16px;border-radius:10px;color:#4dabf7;'>
            Enter current conditions on the left and click
            <b>Forecast Air Quality</b> to get a multi-horizon
            prediction with health advisory.
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align:center;color:gray;font-size:14px;'>
🌐 GitHub: https://github.com/manojkulkarni123/-Air-Quality-Forecaster<br>
© 2026 Air Quality Forecaster
</div>
""", unsafe_allow_html=True)
