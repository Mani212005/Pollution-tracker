
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def display_aqi_trends(raw_data_df, forecasted_pm25_values=None):
    """
    Displays time series plots for PM2.5, showing historical trends and forecasted values.
    Allows selection of historical periods (1 day, 7 days, 30 days).
    """
    st.markdown("#### PM2.5 Trend and Historical Data")

    # Period selection
    period = st.radio(
        "Select Historical Period:",
        ("Last 24 Hours", "Last 7 Days", "Last 30 Days"),
        horizontal=True
    )

    num_history_points = 0
    freq = 'H' # Default to hourly

    if period == "Last 24 Hours":
        num_history_points = 24
        freq = 'H'
    elif period == "Last 7 Days":
        num_history_points = 7 * 24
        freq = 'H'
    elif period == "Last 30 Days":
        num_history_points = 30 * 24
        freq = 'H'

    current_time = pd.to_datetime('now')
    history_dates = pd.date_range(end=current_time, periods=num_history_points, freq=freq)
    
    # Simulate a trend for historical data
    np.random.seed(42) # for reproducibility
    historical_pm25 = np.random.normal(loc=100, scale=20, size=num_history_points)
    historical_pm25 = np.maximum(50, historical_pm25) # Ensure PM2.5 is not too low

    historical_df = pd.DataFrame({
        'timestamp': history_dates,
        'PM2.5': historical_pm25
    })

    # Add current data point if available
    current_pm25 = None
    if not raw_data_df.empty and 'pm25' in raw_data_df.columns:
        current_pm25 = raw_data_df['pm25'].iloc[0]
        current_timestamp = raw_data_df['timestamp'].iloc[0] if 'timestamp' in raw_data_df.columns else pd.to_datetime('now')
        current_data_point = pd.DataFrame({
            'timestamp': [current_timestamp],
            'PM2.5': [current_pm25]
        })
        historical_df = pd.concat([historical_df, current_data_point]).drop_duplicates(subset=['timestamp']).sort_values('timestamp')

    plot_df = historical_df.copy()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=plot_df['timestamp'],
        y=plot_df['PM2.5'],
        mode='lines+markers',
        name='PM2.5 (Historical & Current)',
        line=dict(color='blue')
    ))

    if forecasted_pm25_values is not None:
        for horizon in sorted(forecasted_pm25_values.keys()):
            forecast_value = forecasted_pm25_values[horizon]
            forecast_time = current_time + pd.Timedelta(hours=horizon)
            
            # Add forecast point to plot_df for consistent x-axis range
            forecast_data_point = pd.DataFrame({
                'timestamp': [forecast_time],
                'PM2.5': [forecast_value]
            })
            plot_df = pd.concat([plot_df, forecast_data_point])

            fig.add_trace(go.Scatter(
                x=[current_time, forecast_time],
                y=[current_pm25 if current_pm25 is not None else historical_pm25[-1], forecast_value],
                mode='lines',
                name=f'PM2.5 (Forecast +{horizon}h)',
                line=dict(color='red', dash='dash')
            ))

        current_time_unix_ms = current_time.timestamp() * 1000
        fig.add_vline(x=current_time_unix_ms, line_width=1, line_dash="dash", line_color="green", annotation_text="Current Time", annotation_position="top right")

    fig.update_layout(
        title='PM2.5 Trend and Forecast',
        xaxis_title='Time',
        yaxis_title='PM2.5 (µg/m³)',
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Time Series Plot Test")
    dummy_raw_data = pd.DataFrame({
        'pm25': [180],
        'temperature': [25],
        'humidity': [60],
        'wind_speed': [5],
        'pressure': [1010],
        'timestamp': [pd.to_datetime('now')]
    })
    forecast_values = {1: 195.2, 3: 200.1, 6: 210.5, 12: 220.0}
    display_aqi_trends(dummy_raw_data, forecasted_pm25_values=forecast_values)
