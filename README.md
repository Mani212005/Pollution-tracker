Air Pollution Forecasting and Alert System

A Streamlit web application that provides real-time air quality and weather data, forecasts PM2.5 levels for multiple future horizons, and offers health alerts and data visualizations.

🌟 Features

Real-time Data: Fetches current PM2.5 and weather data from the World Air Quality Index (WAQI).

Multi-Horizon Forecasting: Utilizes machine learning models to predict PM2.5 concentrations at 1, 3, 6, and 12-hour intervals.

AQI Calculation: Converts PM2.5 values into a user-friendly Air Quality Index (AQI) with corresponding health categories.

Health Alerts: Displays actionable health recommendations based on the forecasted 1-hour PM2.5 level.

Interactive Map: Visualizes the current air quality on a map centered on the selected city.

Data Visualization:

AQI Trends: Plots historical and forecasted PM2.5 values.

Feature Importance: Shows which factors are most influential in the model's predictions.

Temporal Heatmap: Visualizes patterns of air quality over time.

Anomaly Detection: Highlights unusual spikes or dips in air quality.

Carbon Footprint Estimator: Includes a tool for users to estimate their carbon footprint.

City Selection: Allows users to choose from a predefined list of major cities.

Dummy Data Fallback: Ensures the application remains functional for demonstration purposes even if the live data API fails.

🛠️ Installation

Clone the repository:

git clone https://github.com/your-username/air-quality-forecast-app.git
cd air-quality-forecast-app


Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


Install the required dependencies:

pip install -r requirements.txt


(Note: You will need to create a requirements.txt file. Based on the provided script, the contents should be at least streamlit, pandas, numpy, and scikit-learn (joblib is part of scikit-learn). You may need to add other libraries used in your utility and component modules.)

Place the pre-trained models and scalers in the model/ directory. The application expects the following file structure:

air_quality_forecast_app/
├── model/
│   ├── air_quality_model_1h.joblib
│   ├── data_scaler_1h.joblib
│   ├── air_quality_model_3h.joblib
│   ├── data_scaler_3h.joblib
│   ├── air_quality_model_6h.joblib
│   ├── data_scaler_6h.joblib
│   ├── air_quality_model_12h.joblib
│   └── data_scaler_12h.joblib
└── ... (rest of the app files)


🚀 Usage

Set up your API keys: The application requires API keys for fetching real-time data. Make sure to have them configured in your environment or within the utils/data_fetching.py file.

Run the Streamlit application:

streamlit run app.py


Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

Select a city from the sidebar to view the air quality forecast and visualizations.

📁 Project Structure

.
├── app.py                   # Main Streamlit application script
├── components/              # Directory for UI components
│   ├── __init__.py
│   ├── carbon_footprint_estimator.py
│   ├── health_alerts.py
│   ├── map_view.py
│   ├── feature_importance.py
│   ├── temporal_heatmap.py
│   ├── time_series_plot.py
│   └── anomaly_detection.py
├── model/                   # Directory to store trained models and scalers
│   ├── air_quality_model_1h.joblib
│   └── ...
├── utils/                   # Directory for utility functions
│   ├── __init__.py
│   ├── data_fetching.py
│   └── preprocess.py
└── README.md                # This file


🤖 Models

The forecasting functionality is powered by machine learning models trained for different prediction horizons (1, 3, 6, and 12 hours). Each model is accompanied by a corresponding data scaler used for preprocessing the input features.

The models are loaded into memory upon the first run and cached for subsequent uses to ensure fast performance.

📝 License

This project is licensed under the MIT License. See the LICENSE file for more details.

🙏 Acknowledgements

Streamlit: For providing an easy-to-use framework for building interactive web applications for data science.

World Air Quality Index (WAQI): For providing the real-time air quality data.
