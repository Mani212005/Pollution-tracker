import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def display_temporal_heatmap(raw_data, city_name, chart_key_prefix=""):
    st.markdown("#### 🗓️ Temporal Heatmap: Daily & Hourly PM2.5 Patterns")
    st.markdown("Identify recurring patterns in air quality throughout the day and across different days.")

    # Generate dummy historical data for demonstration
    # In a real application, this would come from a database or historical API
    num_days = 30
    dates = pd.date_range(end=pd.to_datetime('now'), periods=num_days, freq='D')
    hours = range(24)

    # Create a DataFrame for the heatmap data
    heatmap_data = []
    for date in dates:
        for hour in hours:
            # Simulate PM2.5 values with some daily and hourly patterns
            # Example: higher PM2.5 in morning/evening, some random noise
            pm25_value = 30 + 20 * np.sin(hour / 24 * 2 * np.pi) + np.random.normal(0, 5)
            if date.weekday() >= 5: # Weekends might have different patterns
                pm25_value += 10 # Slightly higher on weekends
            
            # Ensure PM25 is non-negative
            pm25_value = max(0, pm25_value)
            
            heatmap_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Hour': hour,
                'PM2.5': pm25_value
            })
    
    heatmap_df = pd.DataFrame(heatmap_data)

    # Create the heatmap
    fig = px.density_heatmap(
        heatmap_df,
        x="Hour",
        y="Date",
        z="PM2.5",
        category_orders={"Hour": list(range(24))}, # Ensure hours are ordered correctly
        color_continuous_scale="Viridis", # Or "Plasma", "Inferno", "Magma", "Cividis"
        title=f"Hourly PM2.5 Patterns for {city_name}",
        labels={"PM2.5": "PM2.5 (µg/m³)"}
    )

    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Date",
        font=dict(family="sans-serif", size=12, color="#7f7f7f"),
        title_font_size=20,
    )

    st.plotly_chart(fig, use_container_width=True, key=f"{chart_key_prefix}temporal_heatmap_{city_name}")