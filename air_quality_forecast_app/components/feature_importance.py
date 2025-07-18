
import streamlit as st
import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def display_feature_importance(model, scaler, processed_data_df):
    """
    Calculates and displays feature importance using SHAP values for the 1-hour forecast model.
    """
    st.markdown("#### Feature Importance (XAI)")
    st.info("This section shows which factors are most influencing the 1-hour PM2.5 forecast.")

    if processed_data_df.empty:
        st.warning("No data available to calculate feature importance.")
        return

    # Ensure the order of features matches training order
    expected_features = [
        'pm25', 'temperature', 'humidity', 'wind_speed', 'pressure',
        'hour', 'day_of_week', 'month',
        'pm25_lag_1', 'pm25_lag_2', 'pm25_lag_3', 'pm25_lag_4'
    ]
    
    # Reindex processed_data_df to ensure correct column order
    for feature in expected_features:
        if feature not in processed_data_df.columns:
            processed_data_df[feature] = 0.0
    processed_data_df = processed_data_df[expected_features]

    # Scale the processed data
    scaled_data = scaler.transform(processed_data_df)
    scaled_data_df = pd.DataFrame(scaled_data, columns=expected_features)

    try:
        # Create a SHAP explainer object
        explainer = shap.TreeExplainer(model)
        
        # Calculate SHAP values for the current prediction
        shap_values = explainer.shap_values(scaled_data_df)

        # Summarize SHAP values (mean absolute SHAP value for each feature)
        # For a single prediction, shap_values will be a 1D array
        if isinstance(shap_values, list): # For multi-output models, shap_values can be a list
            shap_values = shap_values[0] # Take the first output if it's a list

        # Create a DataFrame for plotting
        feature_importance_df = pd.DataFrame({
            'Feature': expected_features,
            'SHAP Value': np.abs(shap_values[0]) # Use absolute SHAP values for magnitude
        })
        feature_importance_df = feature_importance_df.sort_values(by='SHAP Value', ascending=False)

        # Plot feature importance
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(feature_importance_df['Feature'], feature_importance_df['SHAP Value'], color='skyblue')
        ax.set_xlabel("Mean Absolute SHAP Value (Impact on Model Output Magnitude)")
        ax.set_title("Top Factors Influencing PM2.5 Forecast")
        plt.gca().invert_yaxis() # Highest impact at the top
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error calculating SHAP values: {e}")
        st.warning("SHAP might not be compatible with the current model or data. Displaying raw feature values instead.")
        st.write("Current input features for prediction:")
        st.dataframe(processed_data_df)

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Feature Importance Test")

    # Dummy model and scaler for testing
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    # Generate some dummy data
    np.random.seed(42)
    X = pd.DataFrame(np.random.rand(100, 10), columns=[f'feature_{i}' for i in range(10)])
    y = np.random.rand(100) * 100

    # Train a dummy model
    dummy_model = RandomForestRegressor(random_state=42)
    dummy_model.fit(X, y)

    # Dummy scaler
    dummy_scaler = StandardScaler()
    dummy_scaler.fit(X)

    # Dummy processed data
    dummy_processed_data = pd.DataFrame(np.random.rand(1, 10), columns=[f'feature_{i}' for i in range(10)])

    # Rename columns to match expected_features in display_feature_importance
    dummy_processed_data.columns = [
        'pm25', 'temperature', 'humidity', 'wind_speed', 'pressure',
        'hour', 'day_of_week', 'month',
        'pm25_lag_1', 'pm25_lag_2'
    ] # Only 10 features, so adjust accordingly

    # Add missing expected features with default values
    for feature in [
        'pm25_lag_3', 'pm25_lag_4'
    ]:
        dummy_processed_data[feature] = 0.0

    display_feature_importance(dummy_model, dummy_scaler, dummy_processed_data)
