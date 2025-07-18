import joblib
import numpy as np
import os

# Dummy class for model loading
class DummyModel:
    def predict(self, data):
        # Return a fixed dummy PM2.5 value
        return np.array([50.0])

# Configuration
MODEL_DIR = 'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model'
forecast_horizons = [1, 3, 6, 12]

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Create and save dummy model files for each forecast horizon
for horizon in forecast_horizons:
    model_filename = os.path.join(MODEL_DIR, f'air_quality_model_{horizon}h.joblib')
    joblib.dump(DummyModel(), model_filename)
    print(f"Dummy model for {horizon}-hour forecast saved to: {model_filename}")

print("All dummy models created.")