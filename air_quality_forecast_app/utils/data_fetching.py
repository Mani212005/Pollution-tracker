import requests
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

def fetch_waqi_data(city='delhi', token=os.getenv('WAQI_API_TOKEN')):
    """Fetches real-time air quality data from WAQI API."""
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={token}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data['status'] == 'ok':
            iaqi = data['data']['iaqi']
            aqi = iaqi.get('aqi', {}).get('v') or data['data'].get('aqi') # Try both paths for AQI
            # Extract relevant data, e.g., PM2.5, temperature, humidity
            pm25 = iaqi.get('pm25', {}).get('v')
            temperature = iaqi.get('t', {}).get('v')
            humidity = iaqi.get('h', {}).get('v')
            pressure = iaqi.get('p', {}).get('v')
            wind_speed = iaqi.get('w', {}).get('v')

            return {
                'aqi': aqi,
                'pm25': pm25,
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'timestamp': pd.to_datetime('now')
            }, None
        else:
            error_msg = data.get('data', 'Unknown error from WAQI API')
            return None, f"Error fetching WAQI data for {city}: {error_msg}"
    except requests.exceptions.RequestException as e:
        return None, f"Network or API request failed for {city}: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred while processing WAQI data for {city}: {e}"

def fetch_openweathermap_data(lat='28.7041', lon='77.1025', api_key='YOUR_OPENWEATHERMAP_API_KEY'):
    """Fetches real-time weather data from OpenWeatherMap API."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        main_data = data.get('main', {})
        wind_data = data.get('wind', {})

        return {
            'temperature': main_data.get('temp'),
            'humidity': main_data.get('humidity'),
            'pressure': main_data.get('pressure'),
            'wind_speed': wind_data.get('speed'),
            'timestamp': pd.to_datetime('now')
        }, None
    except requests.exceptions.RequestException as e:
        return None, f"Network or API request failed for OpenWeatherMap: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred while processing OpenWeatherMap data: {e}"

def get_realtime_data(city='delhi'):
    """Combines data from various sources to get real-time air quality and weather data."""
    waqi_data, waqi_error = fetch_waqi_data(city=city)
    # openweather_data, openweather_error = fetch_openweathermap_data() # Uncomment if you want to use OpenWeatherMap

    combined_data = {}
    error_messages = []

    if waqi_data:
        combined_data.update(waqi_data)
    elif waqi_error:
        error_messages.append(waqi_error)
    
    # if openweather_data: # Uncomment if you want to use OpenWeatherMap
    #     combined_data.update(openweather_data)
    # elif openweather_error:
    #     error_messages.append(openweather_error)

    if combined_data:
        # Convert to DataFrame for consistency with model input
        df = pd.DataFrame([combined_data])
        return df, None
    else:
        return pd.DataFrame(), "; ".join(error_messages) if error_messages else "Failed to fetch any real-time data."

if __name__ == '__main__':
    # Example usage:
    data, error = get_realtime_data(city='delhi')
    if data is not None and not data.empty:
        print("Fetched Real-time Data:")
        print(data)
    else:
        print(f"Failed to fetch real-time data: {error}")

    data_invalid, error_invalid = get_realtime_data(city='invalidcity123')
    if data_invalid is not None and not data_invalid.empty:
        print("Fetched Real-time Data for invalid city (should not happen):")
        print(data_invalid)
    else:
        print(f"Failed to fetch real-time data for invalid city: {error_invalid}")