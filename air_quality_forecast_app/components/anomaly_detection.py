import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def display_anomaly_detection(forecasted_pm25_value, raw_data, city_name, chart_key_prefix=""):
    st.markdown("#### 🔍 Anomaly Detection")
    st.markdown("Identify unusual spikes or dips in air quality data that might indicate anomalies.")

    # Generate dummy historical data for demonstration
    num_points = 100
    historical_pm25 = np.random.normal(loc=50, scale=10, size=num_points) # Normal distribution
    timestamps = pd.date_range(end=pd.to_datetime('now'), periods=num_points, freq='H')
    historical_df = pd.DataFrame({'timestamp': timestamps, 'pm25': historical_pm25})

    # Introduce a dummy anomaly for demonstration
    anomaly_index = np.random.randint(20, 80)
    historical_df.loc[anomaly_index, 'pm25'] = np.random.uniform(150, 200) # High anomaly

    # Simple anomaly detection: values significantly higher than the mean
    mean_pm25 = historical_df['pm25'].mean()
    std_pm25 = historical_df['pm25'].std()
    threshold = mean_pm25 + (2 * std_pm25) # 2 standard deviations above mean

    anomalies = historical_df[historical_df['pm25'] > threshold]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=historical_df['timestamp'],
        y=historical_df['pm25'],
        mode='lines',
        name='Historical PM2.5',
        line=dict(color='blue')
    ))

    if not anomalies.empty:
        fig.add_trace(go.Scatter(
            x=anomalies['timestamp'],
            y=anomalies['pm25'],
            mode='markers',
            name='Anomalies',
            marker=dict(color='red', size=10)
        ))

    fig.update_layout(
        title='PM2.5 Anomaly Detection',
        xaxis_title='Time',
        yaxis_title='PM2.5 (µg/m³)',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True, key=f"{chart_key_prefix}anomaly_detection_{city_name}")

    if forecasted_pm25_value is not None and forecasted_pm25_value > threshold:
        st.warning(f"**Potential Anomaly Detected in 1-hour Forecast:** The forecasted PM2.5 ({forecasted_pm25_value:.2f} µg/m³) is unusually high.")
    else:
        st.info("No significant anomalies detected in the 1-hour forecast.")