import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Configuration
MODEL_DIR = 'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model'
FEATURES_TO_SCALE = ['pm25', 'temperature', 'humidity', 'wind_speed', 'pressure']
forecast_horizons = [1, 3, 6, 12]

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Generate dummy historical data for scaler training
# In a real scenario, you would load your actual historical data here.
num_samples = 1000
dummy_historical_data = pd.DataFrame({
    'pm25': np.random.uniform(0, 200, num_samples),
    'temperature': np.random.uniform(-10, 40, num_samples),
    'humidity': np.random.uniform(20, 100, num_samples),
    'wind_speed': np.random.uniform(0, 20, num_samples),
    'pressure': np.random.uniform(980, 1040, num_samples),
})

print("Generated dummy historical data for scaler training.")
print(f"Shape: {dummy_historical_data.shape}")

# Train and save a scaler for each forecast horizon
# In many cases, a single scaler trained on all features is sufficient for all horizons.
# We'll create one for each horizon for consistency with the app's loading logic.
for horizon in forecast_horizons:
    scaler = StandardScaler()
    scaler.fit(dummy_historical_data[FEATURES_TO_SCALE])
    scaler_filename = os.path.join(MODEL_DIR, f'data_scaler_{horizon}h.joblib')
    joblib.dump(scaler, scaler_filename)
    print(f"Dummy scaler for {horizon}-hour forecast saved to: {scaler_filename}")

print("All dummy scalers created.")