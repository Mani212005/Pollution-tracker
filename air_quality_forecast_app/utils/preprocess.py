import pandas as pd
import numpy as np

def preprocess_data(df):
    # In a real application, this function would perform more complex preprocessing steps
    # such as handling missing values, feature engineering, and scaling.
    # For now, we assume the raw data is in a suitable format for the scaler.
    
    # Ensure all expected columns are present, fill with NaN if not
    expected_columns = ['pm25', 'temperature', 'humidity', 'wind_speed', 'pressure']
    for col in expected_columns:
        if col not in df.columns:
            df[col] = np.nan

    # Select and reorder columns to match expected input for the model/scaler
    processed_df = df[expected_columns].copy()
    
    # Handle potential NaN values before scaling (e.g., fill with 0 or mean/median)
    # For simplicity, we'll fill with 0 for now. In a real scenario, more robust imputation is needed.
    processed_df = processed_df.fillna(0)

    return processed_df