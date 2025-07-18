import pandas as pd

def preprocess_data(df):
    """
    Preprocesses raw air quality and weather data for model prediction.
    Assumes input DataFrame has columns like 'pm25', 'temperature', 'humidity', 'wind_speed', 'pressure'.
    Adds time-based features and handles missing values.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    # Ensure timestamp is datetime type
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Add time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
    else:
        # If no timestamp, create dummy time features (e.g., for single real-time prediction)
        current_time = pd.to_datetime('now')
        df['hour'] = current_time.hour
        df['day_of_week'] = current_time.dayofweek
        df['month'] = current_time.month

    # Handle missing values (simple imputation for demonstration)
    for col in ['pm25', 'temperature', 'humidity', 'wind_speed', 'pressure']:
        if col not in df.columns:
            df[col] = 0.0 # Or a more appropriate default/mean/median
        df[col] = df[col].fillna(df[col].mean() if not df[col].isnull().all() else 0.0)

    # Add lag features for PM2.5. For real-time single point prediction,
    # we'll use the current pm25 as a placeholder for lags if no historical context is available.
    # In a real system, this would come from a historical data store.
    for i in range(1, 5): # Lag up to 4 hours
        lag_col = f'pm25_lag_{i}'
        if lag_col not in df.columns:
            # If no historical data, use current pm25 as a simple placeholder for lags
            df[lag_col] = df['pm25'] if 'pm25' in df.columns and not df['pm25'].empty else 0.0


    # Select features that the model expects
    # These should match the features used during model training in train_model.py
    features = [
        'pm25', 'temperature', 'humidity', 'wind_speed', 'pressure',
        'hour', 'day_of_week', 'month',
        'pm25_lag_1', 'pm25_lag_2', 'pm25_lag_3', 'pm25_lag_4'
    ]

    # Ensure all expected features are present, fill with 0 if not (or a more suitable default)
    for feature in features:
        if feature not in df.columns:
            df[feature] = 0.0

    return df[features]

if __name__ == '__main__':
    # Example usage:
    dummy_raw_data = pd.DataFrame({
        'pm25': [150],
        'temperature': [25],
        'humidity': [60],
        'wind_speed': [5],
        'pressure': [1010],
        'timestamp': [pd.to_datetime('2023-01-01 10:00:00')]
    })
    processed_df = preprocess_data(dummy_raw_data)
    print("Processed Data:")
    print(processed_df)

    # Example with missing data and no timestamp
    dummy_raw_data_no_ts = pd.DataFrame({
        'pm25': [150],
        'temperature': [25],
        'humidity': [60],
        'wind_speed': [5],
        'pressure': [1010],
    })
    processed_df_no_ts = preprocess_data(dummy_raw_data_no_ts)
    print("\nProcessed Data (no timestamp, missing values):")
    print(processed_df_no_ts)