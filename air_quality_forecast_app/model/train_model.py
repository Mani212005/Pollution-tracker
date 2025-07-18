

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import lightgbm as lgb

def generate_dummy_data(num_samples=8760 * 2, forecast_horizons=[1, 3, 6, 12]): # 2 years of hourly data
    """Generates more realistic dummy air quality and weather data for model training."""
    np.random.seed(42)
    dates = pd.date_range(start='2022-01-01', periods=num_samples, freq='H')
    df = pd.DataFrame({'timestamp': dates})

    # Base PM2.5 with a general trend and seasonality
    df['pm25'] = 100 + 50 * np.sin(df['timestamp'].dt.dayofyear * (2 * np.pi / 365)) \
                 + 30 * np.sin(df['timestamp'].dt.hour * (2 * np.pi / 24)) \
                 + np.random.normal(0, 10, num_samples) # Yearly, daily cycles + noise
    
    # Simulate higher pollution in winter months (e.g., Nov-Feb)
    df['month'] = df['timestamp'].dt.month
    df.loc[df['month'].isin([11, 12, 1, 2]), 'pm25'] += np.random.normal(50, 20, df[df['month'].isin([11, 12, 1, 2])].shape[0])

    # Ensure PM2.5 is non-negative
    df['pm25'] = np.maximum(20, df['pm25'])

    # Meteorological data with some correlation to PM2.5
    df['temperature'] = 25 - 10 * np.sin(df['timestamp'].dt.dayofyear * (2 * np.pi / 365)) \
                         + np.random.normal(0, 3, num_samples) # Inverse correlation with PM2.5 seasonality
    df['temperature'] = np.maximum(5, df['temperature'])

    df['humidity'] = 60 + 15 * np.sin(df['timestamp'].dt.dayofyear * (2 * np.pi / 365) + np.pi/2) \
                      + np.random.normal(0, 5, num_samples) # Some correlation
    df['humidity'] = np.clip(df['humidity'], 30, 90)

    df['wind_speed'] = 5 + 3 * np.random.rand(num_samples) - (df['pm25'] / 100) * 2 # Inverse correlation with PM2.5
    df['wind_speed'] = np.maximum(0.5, df['wind_speed'])

    df['pressure'] = 1010 + 5 * np.random.normal(0, 1, num_samples)

    # Add time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month

    # Add lag features for PM2.5
    for i in range(1, 5): # Lag up to 4 hours
        df[f'pm25_lag_{i}'] = df['pm25'].shift(i)

    # Create target variables for multiple forecast horizons
    for horizon in forecast_horizons:
        df[f'pm25_next_{horizon}_hour'] = df['pm25'].shift(-horizon)

    return df.dropna()

def train_models(model_type='xgboost', forecast_horizons=[1, 3, 6, 12]):
    """
    Trains air quality forecasting models for multiple horizons and saves them.
    """
    print(f"Generating more realistic dummy data for training...")
    df = generate_dummy_data(forecast_horizons=forecast_horizons)

    features = ['pm25', 'temperature', 'humidity', 'wind_speed', 'pressure', 
                'hour', 'day_of_week', 'month']
    for i in range(1, 5):
        features.append(f'pm25_lag_{i}')

    models = {}
    scalers = {}

    for horizon in forecast_horizons:
        target = f'pm25_next_{horizon}_hour'
        
        X = df[features]
        y = df[target]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        print(f"Training {model_type} model for {horizon}-hour forecast...")
        if model_type == 'xgboost':
            model = XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
        elif model_type == 'lightgbm':
            model = lgb.LGBMRegressor(objective='regression', n_estimators=100, random_state=42)
        else:
            raise ValueError("model_type must be 'xgboost' or 'lightgbm'")

        model.fit(X_train_scaled, y_train)

        # Evaluate (simple evaluation for now)
        train_rmse = np.sqrt(np.mean((model.predict(X_train_scaled) - y_train)**2))
        test_rmse = np.sqrt(np.mean((model.predict(X_test_scaled) - y_test)**2))
        print(f"Train RMSE ({horizon}h): {train_rmse:.2f}")
        print(f"Test RMSE ({horizon}h): {test_rmse:.2f}")

        # Save model and scaler
        model_path = f'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model/air_quality_model_{horizon}h.joblib'
        scaler_path = f'C:/Users/hp/OneDrive/Documents/python/Cleanair/air_quality_forecast_app/model/data_scaler_{horizon}h.joblib'

        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        print(f"Model saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
        
        models[horizon] = model
        scalers[horizon] = scaler

if __name__ == "__main__":
    train_models(model_type='xgboost')
