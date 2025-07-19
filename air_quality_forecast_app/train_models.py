import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Configuration
MODEL_DIR = 'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model'
forecast_horizons = [1, 3, 6, 12]
FEATURES = ['temperature', 'humidity', 'wind_speed', 'pressure']

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

print("Starting model training with synthetic data...")

# Generate synthetic historical data
# In a real scenario, you would load your actual historical data here.
num_samples = 2000 # More samples for better dummy training

data = {
    'pm25': np.random.uniform(0, 200, num_samples),
    'temperature': np.random.uniform(-10, 40, num_samples),
    'humidity': np.random.uniform(20, 100, num_samples),
    'wind_speed': np.random.uniform(0, 20, num_samples),
    'pressure': np.random.uniform(980, 1040, num_samples),
}
historical_df = pd.DataFrame(data)

print(f"Generated synthetic historical data with shape: {historical_df.shape}")

# Prepare features (X) and target (y) for training
X = historical_df[FEATURES]

for horizon in forecast_horizons:
    print(f"\nTraining for {horizon}-hour forecast...")

    # For simplicity, let's assume the target for prediction is just a slightly varied current PM2.5
    # In a real scenario, you would shift your PM2.5 column by the horizon for actual future prediction.
    # For dummy training, we'll just add some noise to the current PM2.5.
    y = historical_df['pm25'] + np.random.normal(0, 5, num_samples) # Target PM2.5 for this horizon

    # Train and save Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    scaler_filename = os.path.join(MODEL_DIR, f'data_scaler_{horizon}h.joblib')
    joblib.dump(scaler, scaler_filename)
    print(f"Scaler saved to: {scaler_filename}")

    # Train and save Model
    model = RandomForestRegressor(n_estimators=10, random_state=42) # Reduced n_estimators for faster dummy training
    model.fit(X_scaled, y)
    model_filename = os.path.join(MODEL_DIR, f'air_quality_model_{horizon}h.joblib')
    joblib.dump(model, model_filename)
    print(f"Model saved to: {model_filename}")

print("\nAll models and scalers trained and saved.")