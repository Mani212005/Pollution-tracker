
import os

base_path = "C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app"
directories = ["model", "utils", "components"]

for directory in directories:
    path = os.path.join(base_path, directory)
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")
