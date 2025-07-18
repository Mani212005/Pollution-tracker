
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def display_temporal_heatmap(historical_df, key_suffix=""):
    """
    Displays a temporal heatmap of PM2.5 by hour of day and day of week.
    """
    st.markdown("#### PM2.5 Temporal Heatmap")

    if historical_df.empty:
        st.info("No historical data available to generate heatmap.")
        return

    # Ensure timestamp is datetime and PM2.5 is numeric
    historical_df['timestamp'] = pd.to_datetime(historical_df['timestamp'])
    historical_df['pm25'] = pd.to_numeric(historical_df['pm25'], errors='coerce')
    historical_df.dropna(subset=['pm25'], inplace=True)

    if historical_df.empty:
        st.info("No valid PM2.5 data after cleaning for heatmap.")
        return

    # Extract hour and day of week
    historical_df['Hour'] = historical_df['timestamp'].dt.hour
    historical_df['Day of Week'] = historical_df['timestamp'].dt.day_name()

    # Order days of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    historical_df['Day of Week'] = pd.Categorical(historical_df['Day of Week'], categories=day_order, ordered=True)

    # Aggregate data: average PM2.5 for each hour-day combination
    heatmap_data = historical_df.groupby(['Day of Week', 'Hour'])['pm25'].mean().unstack()

    fig = px.imshow(heatmap_data,
                    labels=dict(x="Hour of Day", y="Day of Week", color="Average PM2.5"),
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title="Average PM2.5 by Hour and Day of Week")

    fig.update_xaxes(side="top")
    st.plotly_chart(fig, use_container_width=True, key=f"temporal_heatmap_{key_suffix}")

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Temporal Heatmap Test")

    # Generate dummy historical data for testing
    num_samples = 24 * 7 * 4 # 4 weeks of hourly data
    dates = pd.date_range(start='2023-01-01', periods=num_samples, freq='H')
    pm25_values = np.random.normal(loc=80, scale=20, size=num_samples)
    pm25_values = np.maximum(20, pm25_values)

    # Add some patterns
    pm25_values += 30 * np.sin(np.arange(num_samples) * (2 * np.pi / 24)) # Daily cycle
    pm25_values += 20 * np.sin(np.arange(num_samples) * (2 * np.pi / (24*7))) # Weekly cycle

    dummy_historical_df = pd.DataFrame({
        'timestamp': dates,
        'PM2.5': pm25_values
    })

    display_temporal_heatmap(dummy_historical_df)
