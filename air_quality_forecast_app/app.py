
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Import utility functions and UI components
from utils.data_fetching import get_realtime_data
from utils.preprocess import preprocess_data
from components.health_alerts import display_health_alert
from components.map_view import display_map
from components.time_series_plot import display_aqi_trends
from components.feature_importance import display_feature_importance
from components.temporal_heatmap import display_temporal_heatmap
from components.anomaly_detection import display_anomaly_detection
from components.carbon_footprint_estimator import display_carbon_footprint_estimator

# --- City Coordinates (for map centering) ---
city_coordinates = {
    "Delhi": {"lat": 28.7041, "lon": 77.1025},
    "London": {"lat": 51.5074, "lon": 0.1278},
    "Beijing": {"lat": 39.9042, "lon": 116.4074},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Tokyo": {"lat": 35.6895, "lon": 139.6917},
}

# --- Model Loading ---
@st.cache_resource
def load_models(forecast_horizons=[1, 3, 6, 12]):
    """Loads the trained ML models and scalers for multiple forecast horizons."""
    models = {}
    scalers = {}
    for horizon in forecast_horizons:
        try:
            model_path = f'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model/air_quality_model_{horizon}h.joblib'
            scaler_path = f'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model/data_scaler_{horizon}h.joblib'
            models[horizon] = joblib.load(model_path)
            scalers[horizon] = joblib.load(scaler_path)
        except FileNotFoundError:
            st.error(f"Model or scaler files not found for {horizon}-hour forecast. Please ensure all models are trained and saved.")
            st.stop()
    return models, scalers

forecast_horizons = [1, 3, 6, 12]
models, scalers = load_models(forecast_horizons)

# --- Prediction Function ---
def run_multi_hour_prediction(raw_data_df, models, scalers, forecast_horizons):
    """
    Runs the prediction pipeline for multiple forecast horizons.
    Returns a dictionary of forecasted PM2.5 values.
    """
    if raw_data_df.empty:
        return {horizon: None for horizon in forecast_horizons}

    processed_df = preprocess_data(raw_data_df)
    
    if processed_df.empty:
        st.warning("Processed data is empty. Cannot make predictions.")
        return {horizon: None for horizon in forecast_horizons}

    forecasted_values = {}
    for horizon in forecast_horizons:
        model = models[horizon]
        scaler = scalers[horizon]

        scaled_data = scaler.transform(processed_df)
        forecast = model.predict(scaled_data)
        forecasted_values[horizon] = forecast[0] # Assuming single prediction for each horizon
    
    return forecasted_values

# --- AQI Calculation (Placeholder) ---
def calculate_aqi(pm25_value):
    """
    Calculates AQI from PM2.5 value based on a simplified scale.
    This is a placeholder and should be replaced with a more accurate AQI calculation.
    """
    if pm25_value is None:
        return "N/A"
    if pm25_value <= 12.0: return "Good"
    elif pm25_value <= 35.4: return "Moderate"
    elif pm25_value <= 55.4: return "Unhealthy for Sensitive Groups"
    elif pm25_value <= 150.4: return "Unhealthy"
    elif pm25_value <= 250.4: return "Very Unhealthy"
    else: return "Hazardous"

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Air Pollution Forecast")

st.title("🌬️ Air Pollution Forecasting and Alert System")

# City Selection
selected_city = st.sidebar.selectbox(
    "Select a City:",
    list(city_coordinates.keys())
)

st.markdown(f"### Real-time PM2.5 and AQI Forecast for {selected_city}")

# Fetch real-time data
st.subheader("1. Fetching Real-time Data")
with st.spinner(f"Fetching latest air quality and weather data for {selected_city}..."):
    raw_data, error_message = get_realtime_data(city=selected_city.lower()) # WAQI uses lowercase city names

if raw_data is not None and not raw_data.empty:
    st.success("Data fetched successfully!")
    st.write("Latest Raw Data:")
    st.dataframe(raw_data)

    # Run multi-hour prediction
    st.subheader("2. Forecasting Air Quality")
    forecasted_pm25_values = run_multi_hour_prediction(raw_data, models, scalers, forecast_horizons)

    if all(value is not None for value in forecasted_pm25_values.values()):
        st.write("#### Forecasted PM2.5 Values:")
        cols = st.columns(len(forecast_horizons))
        for i, horizon in enumerate(forecast_horizons):
            with cols[i]:
                st.metric(label=f"PM2.5 (+{horizon}h)", value=f"{forecasted_pm25_values[horizon]:.2f} µg/m³")
                st.write(f"AQI: {calculate_aqi(forecasted_pm25_values[horizon])}")

        # Display health alerts for the 1-hour forecast
        st.subheader("3. Health Alerts (1-hour forecast)")
        display_health_alert(forecasted_pm25_values[1])

        # Display visualizations
        st.subheader("4. Visualizations")
        display_map(forecasted_pm25_values[1], city_coordinates[selected_city]["lat"], city_coordinates[selected_city]["lon"]) # Pass 1-hour forecast and city coords to map
        display_aqi_trends(raw_data, forecasted_pm25_values) # Pass all forecasts to trend plot
        display_feature_importance(models[1], scalers[1], raw_data) # Pass 1-hour model, scaler, and raw data
        display_temporal_heatmap(raw_data) # Pass raw_data for now, will use dummy historical data within the component
        display_anomaly_detection(forecasted_pm25_values[1], raw_data) # Pass 1-hour forecast and raw_data for historical context

        st.subheader("5. Carbon Footprint Estimator")
        display_carbon_footprint_estimator()

    else:
        st.error("Could not generate all forecasts. Please check data fetching and preprocessing.")
else:
    st.error("Failed to fetch real-time data. Please check your API keys and internet connection.")
    st.info("Using dummy data for demonstration purposes if real data cannot be fetched.")
    # Fallback to dummy data for demonstration if API fails
    dummy_data = pd.DataFrame({
        'pm25': [150],
        'temperature': [25],
        'humidity': [60],
        'wind_speed': [5],
        'pressure': [1010],
        'timestamp': [pd.to_datetime('now')]
    })
    st.write("Using Dummy Data for Forecast:")
    st.dataframe(dummy_data)
    forecasted_pm25_values_dummy = run_multi_hour_prediction(dummy_data, models, scalers, forecast_horizons)
    if all(value is not None for value in forecasted_pm25_values_dummy.values()):
        st.write("#### Forecasted PM2.5 Values (Dummy Data):")
        cols = st.columns(len(forecast_horizons))
        for i, horizon in enumerate(forecast_horizons):
            with cols[i]:
                st.metric(label=f"PM2.5 (+{horizon}h)", value=f"{forecasted_pm25_values_dummy[horizon]:.2f} µg/m³")
                st.write(f"AQI: {calculate_aqi(forecasted_pm25_values_dummy[horizon])}")
        display_health_alert(forecasted_pm25_values_dummy[1])
