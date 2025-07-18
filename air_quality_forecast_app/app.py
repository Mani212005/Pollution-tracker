import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px

# Inject custom CSS for styling
with open('styles/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Import utility functions and UI components
from utils.data_fetching import get_realtime_data
from utils.preprocess import preprocess_data
from components.health_alerts import display_health_alert
from components.map_view import display_map, get_aqi_category
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

def display_city_data(selected_city, chart_key_prefix, current_mode):
    """Fetches and displays the data for a single city."""
    
    with st.container(): # Wrap the entire city display in a container for responsiveness
        # Adjust section titles based on mode for conciseness in comparison view
        if current_mode == "City Comparison":
            data_acquisition_title = "📊 Data Acquisition"
            forecasting_title = "📈 Forecasting"
            health_alerts_title = "🚨 Health Advisory"
            visualizations_title = "📊 Visualizations"
        else:
            data_acquisition_title = "📊 Real-time Data Acquisition"
            forecasting_title = "📈 Air Quality Forecasting"
            health_alerts_title = "🚨 Health Advisory"
            visualizations_title = "📊 Insightful Visualizations"

        st.subheader(f"Air Quality for {selected_city}") # Use st.subheader for city title

        # Section 1: Real-time Data Fetching
        st.container(border=True).markdown(f"### {data_acquisition_title}")
        with st.container(border=True):
            st.markdown(f"#### Fetching latest air quality and weather data for {selected_city}...")
            with st.spinner("Connecting to data sources..."):
                raw_data, error_message = get_realtime_data(city=selected_city.lower()) # WAQI uses lowercase city names

            if raw_data is not None and not raw_data.empty:
                st.success("Data fetched successfully!")
                with st.expander("View Raw Data and Visualization"):
                    st.write("Latest Raw Data:")
                    st.dataframe(raw_data, use_container_width=True) # Ensure responsiveness
                    st.write("Raw Data Visualization:")
                    st.plotly_chart(create_raw_data_chart(raw_data), use_container_width=True, key=f"{chart_key_prefix}raw_data_chart_{selected_city}")
            else:
                st.error("Failed to fetch real-time data. Please check your API keys and internet connection.")
                st.info("Using dummy data for demonstration purposes if real data cannot be fetched.")
                # Fallback to dummy data for demonstration if API fails
                raw_data = pd.DataFrame({
                    'pm25': [150],
                    'temperature': [25],
                    'humidity': [60],
                    'wind_speed': [5],
                    'pressure': [1010],
                    'timestamp': [pd.to_datetime('now')]
                })
                st.write("Using Dummy Data for Forecast:")
                st.dataframe(raw_data, use_container_width=True) # Ensure responsiveness

        # Section 2: Air Quality Forecasting
        st.container(border=True).markdown(f"### {forecasting_title}")
        with st.container(border=True):
            forecasted_pm25_values = run_multi_hour_prediction(raw_data, models, scalers, forecast_horizons)

            if all(value is not None for value in forecasted_pm25_values.values()):
                st.markdown("#### Forecasted PM2.5 Values:")
                cols = st.columns(len(forecast_horizons))
                for i, horizon in enumerate(forecast_horizons):
                    with cols[i]:
                        st.metric(label=f"PM2.5 (+{horizon}h)", value=f"{forecasted_pm25_values[horizon]:.2f} µg/m³")
                        st.write(f"AQI: {calculate_aqi(forecasted_pm25_values[horizon])}")
            else:
                st.error("Could not generate all forecasts. Please check data fetching and preprocessing.")

        # Section 3: Health Alerts
        st.container(border=True).markdown(f"### {health_alerts_title}")
        with st.container(border=True):
            display_health_alert(forecasted_pm25_values[1])

        # Section 4: Visualizations
        st.container(border=True).markdown(f"### {visualizations_title}")
        with st.container(border=True):
            # Prepare data for map: current city + dummy nearby locations
            map_locations = [{
                'City': selected_city,
                'Latitude': city_coordinates[selected_city]["lat"],
                'Longitude': city_coordinates[selected_city]["lon"],
                'PM2.5': forecasted_pm25_values[1], # Use 1-hour forecast for map
                'AQI_Category': get_aqi_category(forecasted_pm25_values[1])
            }]

            # Add dummy nearby locations for demonstration in Single City Analysis mode
            if current_mode == "Single City Analysis":
                map_locations.append({
                    'City': 'Nearby A',
                    'Latitude': city_coordinates[selected_city]["lat"] + 0.1,
                    'Longitude': city_coordinates[selected_city]["lon"] + 0.1,
                    'PM2.5': forecasted_pm25_values[1] * 1.2, # Slightly higher pollution
                    'AQI_Category': get_aqi_category(forecasted_pm25_values[1] * 1.2)
                })
                map_locations.append({
                    'City': 'Nearby B',
                    'Latitude': city_coordinates[selected_city]["lat"] - 0.05,
                    'Longitude': city_coordinates[selected_city]["lon"] + 0.08,
                    'PM2.5': forecasted_pm25_values[1] * 0.8, # Slightly lower pollution
                    'AQI_Category': get_aqi_category(forecasted_pm25_values[1] * 0.8)
                })
            
            map_data_df = pd.DataFrame(map_locations)
            display_map(map_data_df, chart_key_prefix) # Pass DataFrame to map
            display_aqi_trends(raw_data, forecasted_pm25_values, selected_city, chart_key_prefix) # Pass all forecasts to trend plot
            display_feature_importance(models[1], scalers[1], raw_data, selected_city, chart_key_prefix) # Pass 1-hour model, scaler, and raw data
            display_temporal_heatmap(raw_data, selected_city, chart_key_prefix) # Pass raw_data for now, will use dummy historical data within the component
            display_anomaly_detection(forecasted_pm25_values[1], raw_data, selected_city, chart_key_prefix) # Pass 1-hour forecast and raw_data for historical context

        # Section 5: Carbon Footprint Estimator (only in Single City Analysis mode)
        if current_mode == "Single City Analysis":
            st.container(border=True).markdown("### 👣 Carbon Footprint Estimator")
            with st.container(border=True):
                display_carbon_footprint_estimator(chart_key_prefix)

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="CleanAir: Air Quality Forecast", page_icon="🌬️")

# Custom header with improved styling
st.markdown('<h1 class="main-title">🌬️ CleanAir: AI-Powered Air Quality Forecasting</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-description">A comprehensive web application providing real-time air quality forecasts, health alerts, and insightful visualizations to empower informed decisions for your well-being.</p>', unsafe_allow_html=True)

st.markdown("---") # Visual separator

# Sidebar for mode and city selection
st.sidebar.header("Navigation")
mode = st.sidebar.radio("Choose Application Mode:", ("Single City Analysis", "City Comparison"), key="mode_selection")

if mode == "Single City Analysis":
    st.sidebar.subheader("Select Your City")
    selected_city = st.sidebar.selectbox(
        "City:",
        list(city_coordinates.keys()),
        key="single_city_select"
    )
    
    st.header(f"Real-time Air Quality for {selected_city}")
    st.markdown("Stay informed about the air you breathe.")
    
    # Main content for single city
    display_city_data(selected_city, "single_city_", mode)

else: # City Comparison Mode
    st.header("Compare Air Quality Between Cities")
    st.markdown("Analyze and compare air quality trends and forecasts for two different locations.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("City 1")
        city1 = st.selectbox("Select City 1", list(city_coordinates.keys()), key='city1_select')
        display_city_data(city1, "city1_", mode)
    with col2:
        st.subheader("City 2")
        city2 = st.selectbox("Select City 2", list(city_coordinates.keys()), key='city2_select')
        display_city_data(city2, "city2_", mode)

st.sidebar.markdown("---")
st.sidebar.subheader("About CleanAir")
st.sidebar.info(
    "CleanAir is designed to empower users with critical information about air quality. "
    "It leverages machine learning models for forecasting and provides actionable health advisories. "
    "Developed with Streamlit, it aims for a user-friendly and interactive experience."
)

st.markdown("<br><br>", unsafe_allow_html=True) # Add some space at the bottom
st.markdown("<footer><p style='text-align: center; color: var(--text-color); opacity: 0.7;'>CleanAir © 2023. All rights reserved.</p></footer>", unsafe_allow_html=True)

