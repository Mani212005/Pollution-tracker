import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_aqi_category(pm25_value):
    if pm25_value is None: return "N/A"
    if pm25_value <= 12.0: return "Good"
    elif pm25_value <= 35.4: return "Moderate"
    elif pm25_value <= 55.4: return "Unhealthy for Sensitive Groups"
    elif pm25_value <= 150.4: return "Unhealthy"
    elif pm25_value <= 250.4: return "Very Unhealthy"
    else: return "Hazardous"

aqi_colors = {
    "Good": "#00E400",  # Green
    "Moderate": "#FFFF00", # Yellow
    "Unhealthy for Sensitive Groups": "#FF7E00", # Orange
    "Unhealthy": "#FF0000", # Red
    "Very Unhealthy": "#8F3F97", # Purple
    "Hazardous": "#7E0023", # Maroon
    "N/A": "#CCCCCC" # Grey for not available
}

def display_map(map_data_df, chart_key_prefix=""):
    st.markdown("#### 🗺️ Interactive Air Quality Map")

    if map_data_df.empty:
        st.info("No data available to display on the map.")
        return

    # Calculate center of the map based on provided data
    center_lat = map_data_df['Latitude'].mean()
    center_lon = map_data_df['Longitude'].mean()

    fig = px.scatter_mapbox(
        map_data_df,
        lat="Latitude",
        lon="Longitude",
        color="AQI_Category", # Color by AQI category
        color_discrete_map=aqi_colors, # Use discrete color map
        size="PM2.5", # Size of marker based on PM2.5 value
        zoom=9, # Adjusted zoom for state-level view
        height=500,
        title="Air Quality Levels Across Selected Locations",
        labels={'PM2.5': 'PM2.5 (µg/m³)', 'AQI_Category': 'AQI Category'},
        mapbox_style="open-street-map", # Changed to a supported map style
        hover_name="City", # Display city name on hover
        hover_data={"PM2.5": True, "AQI_Category": True, "Latitude": False, "Longitude": False} # Show PM2.5 and AQI on hover
    )

    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        legend_title_text='AQI Category',
        mapbox=dict(
            center=go.layout.mapbox.Center(lat=center_lat, lon=center_lon),
            zoom=fig.layout.mapbox.zoom # Keep initial zoom or adjust as needed
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=f"{chart_key_prefix}map_view")

    st.markdown("**Note:** Marker size indicates PM2.5 levels. Colors represent AQI categories as per the legend. Hover over markers for details.")