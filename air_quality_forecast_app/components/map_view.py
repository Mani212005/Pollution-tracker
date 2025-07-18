
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def generate_dummy_sensor_data(num_sensors=10, center_lat=28.7041, center_lon=77.1025):
    """
    Generates dummy sensor data for demonstration purposes around a given center point.
    """
    np.random.seed(42)
    
    # Approximate bounds around the center for dummy sensors
    lat_range = 0.2 # degrees
    lon_range = 0.2 # degrees

    lats = np.random.uniform(center_lat - lat_range, center_lat + lat_range, num_sensors)
    lons = np.random.uniform(center_lon - lon_range, center_lon + lon_range, num_sensors)
    pm25_values = np.random.uniform(20, 350, num_sensors) # Varying PM2.5 levels

    data = []
    for i in range(num_sensors):
        pm25 = pm25_values[i]
        aqi_category, color = get_aqi_category_and_color(pm25)
        data.append({
            'Sensor ID': f'Sensor {i+1}',
            'lat': lats[i],
            'lon': lons[i],
            'PM2.5': pm25,
            'AQI Category': aqi_category,
            'Color': color
        })
    return pd.DataFrame(data)

def get_aqi_category_and_color(pm25_value):
    """
    Determines AQI category and corresponding color based on PM2.5 value.
    Using US EPA PM2.5 breakpoints.
    """
    if pm25_value <= 12.0:
        return "Good", "green"
    elif pm25_value <= 35.4:
        return "Moderate", "yellow"
    elif pm25_value <= 55.4:
        return "Unhealthy for Sensitive Groups", "orange"
    elif pm25_value <= 150.4:
        return "Unhealthy", "red"
    elif pm25_value <= 250.4:
        return "Very Unhealthy", "purple"
    else:
        return "Hazardous", "maroon"

def display_map(forecasted_pm25=None, center_lat=28.7041, center_lon=77.1025):
    """
    Displays a map with simulated air quality sensor data, centered on the given coordinates.
    """
    st.markdown("#### Real-time Air Quality Map")

    sensor_df = generate_dummy_sensor_data(center_lat=center_lat, center_lon=center_lon)

    fig = px.scatter_mapbox(
        sensor_df,
        lat="lat",
        lon="lon",
        color="AQI Category", # Color markers by AQI category
        color_discrete_map={
            "Good": "green",
            "Moderate": "yellow",
            "Unhealthy for Sensitive Groups": "orange",
            "Unhealthy": "red",
            "Very Unhealthy": "purple",
            "Hazardous": "maroon"
        },
        size="PM2.5", # Size markers by PM2.5 value
        size_max=30,
        zoom=9, # Zoom level
        height=500,
        hover_name="Sensor ID",
        hover_data={'PM2.5': ':.2f', 'AQI Category': True, 'lat':False, 'lon':False, 'Color':False},
        title=f"Air Quality Sensors (Simulated Data) near {center_lat:.2f}, {center_lon:.2f}"
    )

    fig.update_layout(mapbox_style="open-street-map", mapbox_center={'lat': center_lat, 'lon': center_lon})
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    st.plotly_chart(fig, use_container_width=True)

    if forecasted_pm25 is not None:
        st.write(f"*Note: Your forecasted PM2.5 for the next hour is: **{forecasted_pm25:.2f} µg/m³***")

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Map View Test")
    display_map(forecasted_pm25=135.5, center_lat=28.7041, center_lon=77.1025)
