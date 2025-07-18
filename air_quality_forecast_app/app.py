
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px

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

def create_raw_data_chart(raw_data):
    """Creates an interactive Plotly bar chart for the raw data."""
    if raw_data.empty:
        return None

    # Melt the dataframe to have a long format for Plotly
    raw_data_melted = raw_data.melt(id_vars=['timestamp'], var_name='Pollutant', value_name='Value')

    fig = px.bar(
        raw_data_melted,
        x='Pollutant',
        y='Value',
        color='Pollutant',
        title='Latest Raw Air Quality and Weather Data',
        labels={'Value': 'Measurement Value', 'Pollutant': 'Pollutant/Metric'},
        template='plotly_white'
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Value",
        font=dict(family="sans-serif", size=12, color="#7f7f7f"),
        title_font_size=20,
    )
    return fig

def display_city_data(selected_city, key_suffix=""):
    """Fetches and displays the data for a single city."""
    st.markdown(f"### Real-time PM2.5 and AQI Forecast for {selected_city}")

    # Fetch real-time data
    st.subheader("1. Fetching Real-time Data")
    with st.spinner(f"Fetching latest air quality and weather data for {selected_city}..."):
        raw_data, error_message = get_realtime_data(city=selected_city.lower()) # WAQI uses lowercase city names

    if raw_data is not None and not raw_data.empty:
        st.success("Data fetched successfully!")
        st.write("Latest Raw Data:")
        st.dataframe(raw_data)

        # Add a bar chart for the raw data
        st.write("Raw Data Visualization:")
        st.plotly_chart(create_raw_data_chart(raw_data), use_container_width=True, key=f"raw_data_chart_{selected_city}_{key_suffix}")

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
            display_health_alert(forecasted_pm25_values[1], key_suffix=key_suffix)

            # Display visualizations
            st.subheader("4. Visualizations")
            display_map(forecasted_pm25_values[1], city_coordinates[selected_city]["lat"], city_coordinates[selected_city]["lon"], key_suffix=key_suffix) # Pass 1-hour forecast and city coords to map
            display_aqi_trends(raw_data, forecasted_pm25_values, key_suffix=key_suffix) # Pass all forecasts to trend plot
            display_feature_importance(models[1], scalers[1], raw_data, key_suffix=key_suffix) # Pass 1-hour model, scaler, and raw data
            display_temporal_heatmap(raw_data, key_suffix=key_suffix) # Pass raw_data for now, will use dummy historical data within the component
            display_anomaly_detection(forecasted_pm25_values[1], raw_data, key_suffix=key_suffix) # Pass 1-hour forecast and raw_data for historical context

            st.subheader("5. Carbon Footprint Estimator")
            display_carbon_footprint_estimator(key_suffix=key_suffix)

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

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Air Pollution Forecast")

st.title("🌬️ Air Pollution Forecasting and Alert System")

# Mode Selection
mode = st.sidebar.radio("Select Mode:", ("Single City", "Compare Cities"))

if mode == "Single City":
    # City Selection
    selected_city = st.sidebar.selectbox(
        "Select a City:",
        list(city_coordinates.keys())
    )
    display_city_data(selected_city, key_suffix="single")
else:
    st.header("City Comparison")
    col1, col2 = st.columns(2)
    with col1:
        city1 = st.selectbox("Select City 1", list(city_coordinates.keys()), key='city1')
        display_city_data(city1, key_suffix="city1")
    with col2:
        city2 = st.selectbox("Select City 2", list(city_coordinates.keys()), key='city2')
        display_city_data(city2, key_suffix="city2")

