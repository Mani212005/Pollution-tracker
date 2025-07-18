import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def display_aqi_trends(raw_data, forecasted_pm25_values, city_name, chart_key_prefix=""):
    st.markdown("#### 📈 AQI Trends: Historical & Forecasted")
    st.markdown("Visualize the historical PM2.5 levels and their forecasted trends.")

    if raw_data.empty:
        st.info("No historical data available to display trends.")
        return

    # Create a dummy historical PM2.5 series for demonstration
    # In a real app, this would come from a database or historical API
    num_historical_points = 24 # Last 24 hours
    historical_timestamps = pd.date_range(end=pd.to_datetime('now'), periods=num_historical_points, freq='H')
    # Simulate some variation around the current raw_data pm25
    historical_pm25 = raw_data['pm25'].iloc[0] + (np.random.rand(num_historical_points) - 0.5) * 20
    historical_df = pd.DataFrame({'timestamp': historical_timestamps, 'pm25': historical_pm25})

    # Append the current raw data point
    current_data_point = pd.DataFrame({
        'timestamp': [raw_data['timestamp'].iloc[0]],
        'pm25': [raw_data['pm25'].iloc[0]]
    })
    historical_df = pd.concat([historical_df, current_data_point]).sort_values('timestamp').reset_index(drop=True)

    # Prepare forecasted data
    forecast_data = []
    current_time = pd.to_datetime('now')
    for horizon, pm25_value in forecasted_pm25_values.items():
        if pm25_value is not None:
            forecast_time = current_time + pd.Timedelta(hours=horizon)
            forecast_data.append({'timestamp': forecast_time, 'pm25': pm25_value})
    forecast_df = pd.DataFrame(forecast_data)

    fig = go.Figure()

    # Add historical trace
    fig.add_trace(go.Scatter(
        x=historical_df['timestamp'],
        y=historical_df['pm25'],
        mode='lines+markers',
        name='Historical PM2.5',
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    # Add forecasted trace
    if not forecast_df.empty:
        fig.add_trace(go.Scatter(
            x=forecast_df['timestamp'],
            y=forecast_df['pm25'],
            mode='lines+markers',
            name='Forecasted PM2.5',
            line=dict(color='red', dash='dash'),
            marker=dict(size=6)
        ))

    fig.update_layout(
        title=f'PM2.5 Trends for {city_name}',
        xaxis_title='Time',
        yaxis_title='PM2.5 (µg/m³)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(x=0.01, y=0.99, bordercolor="Black", borderwidth=1)
    )

    st.plotly_chart(fig, use_container_width=True, key=f"{chart_key_prefix}aqi_trends_{city_name}")