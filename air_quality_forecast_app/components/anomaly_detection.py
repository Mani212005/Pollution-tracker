import streamlit as st
import pandas as pd
import numpy as np

def display_anomaly_detection(current_pm25, historical_pm25_data=None, key_suffix=""):
    """
    Performs a basic anomaly detection on the current PM2.5 value
    compared to historical data (if available) or a predefined threshold.
    """
    st.markdown("#### Anomaly Detection")

    is_anomaly = False
    anomaly_message = "No anomalies detected based on current data."

    if current_pm25 is None:
        st.info("Current PM2.5 data not available for anomaly detection.")
        return

    # Using a simple statistical approach for demonstration
    # In a real application, you'd use more robust methods and more historical data.
    
    # Option 1: Compare to a fixed threshold (simple)
    if current_pm25 > 300: # Example threshold for severe pollution
        is_anomaly = True
        anomaly_message = f"**HIGH PM2.5 ANOMALY:** Current PM2.5 ({current_pm25:.2f}) is extremely high!"

    # Option 2: Compare to historical mean/std (if historical data is provided)
    if historical_pm25_data is not None and not historical_pm25_data.empty:
        # Ensure pm25 is numeric
        historical_pm25_data['pm25'] = pd.to_numeric(historical_pm25_data['pm25'], errors='coerce')
        historical_pm25_data.dropna(subset=['pm25'], inplace=True)

        if not historical_pm25_data.empty:
            mean_pm25 = historical_pm25_data['pm25'].mean()
            std_pm25 = historical_pm25_data['pm25'].std()

            # Define anomaly as more than 3 standard deviations from the mean
            if std_pm25 > 0 and (current_pm25 > (mean_pm25 + 3 * std_pm25) or current_pm25 < (mean_pm25 - 3 * std_pm25)):
                is_anomaly = True
                anomaly_message = f"**STATISTICAL ANOMALY:** Current PM2.5 ({current_pm25:.2f}) is significantly different from historical average ({mean_pm25:.2f} ± {std_pm25:.2f})."

    if is_anomaly:
        st.warning(anomaly_message)
    else:
        st.success(anomaly_message)

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Anomaly Detection Test")

    # Dummy historical data for testing
    num_samples = 24 * 7 # 1 week of hourly data
    dates = pd.date_range(start='2023-01-01', periods=num_samples, freq='H')
    historical_pm25 = np.random.normal(loc=80, scale=10, size=num_samples)
    historical_pm25 = np.maximum(20, historical_pm25)
    dummy_historical_df = pd.DataFrame({
        'timestamp': dates,
        'pm25': historical_pm25
    })

    st.subheader("Test Case 1: Normal Value")
    display_anomaly_detection(current_pm25=85.0, historical_pm25_data=dummy_historical_df)

    st.subheader("Test Case 2: High Anomaly (Fixed Threshold)")
    display_anomaly_detection(current_pm25=350.0, historical_pm25_data=dummy_historical_df)

    st.subheader("Test Case 3: Statistical Anomaly (High)")
    display_anomaly_detection(current_pm25=150.0, historical_pm25_data=dummy_historical_df)

    st.subheader("Test Case 4: Statistical Anomaly (Low)")
    display_anomaly_detection(current_pm25=10.0, historical_pm25_data=dummy_historical_df)