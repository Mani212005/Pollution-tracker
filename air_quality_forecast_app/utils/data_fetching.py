import pandas as pd
import requests

WAQI_API_TOKEN = "de2414f3929aab0fdca4e231434fd227c29a7bce"

def get_realtime_data(city):
    try:
        url = f"https://api.waqi.info/feed/{city}/?token={WAQI_API_TOKEN}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if data and data["status"] == "ok":
            iaqi = data["data"]["iaqi"]
            # Extract relevant parameters, handling missing ones
            pm25 = iaqi["pm25"]["v"] if "pm25" in iaqi else None
            temperature = iaqi["t"]["v"] if "t" in iaqi else None
            humidity = iaqi["h"]["v"] if "h" in iaqi else None
            wind_speed = iaqi["w"]["v"] if "w" in iaqi else None
            pressure = iaqi["p"]["v"] if "p" in iaqi else None

            # Create a DataFrame
            df = pd.DataFrame({
                'pm25': [pm25],
                'temperature': [temperature],
                'humidity': [humidity],
                'wind_speed': [wind_speed],
                'pressure': [pressure],
                'timestamp': [pd.to_datetime('now')]
            })
            return df, None
        else:
            return None, f"Error fetching data from WAQI: {data.get("data", "Unknown error")}"
    except requests.exceptions.RequestException as e:
        return None, f"Network or API error: {e}"
    except KeyError as e:
        return None, f"Error parsing WAQI data (missing key): {e}. Response: {data}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"