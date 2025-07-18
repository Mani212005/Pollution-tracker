# CleanAir: AI-Powered Air Quality Forecasting & Health Advisory System

CleanAir is a comprehensive web application built with Streamlit that provides real-time air quality forecasting, health alerts, and insightful visualizations. Leveraging machine learning, this tool empowers users to stay informed about air pollution levels and make data-driven decisions for their health and well-being.

## 🚀 Features

- **Real-time Data Integration:** Fetches live air quality and weather data from global monitoring stations.
- **Multi-Horizon Forecasting:** Predicts PM2.5 concentrations at 1, 3, 6, and 12-hour intervals using advanced machine learning models.
- **Dynamic AQI Calculation:** Converts PM2.5 forecasts into easy-to-understand Air Quality Index (AQI) levels.
- **Automated Health Alerts:** Generates timely health advisories and recommendations based on forecasted pollution levels.
- **Interactive Map View:** Visualizes air quality data on an interactive map, centered on user-selected cities.
- **Insightful Visualizations:**
  - **Time-Series Analysis:** Tracks historical and forecasted AQI trends.
  - **Feature Importance:** Reveals the key environmental factors influencing air quality.
  - **Temporal Heatmaps:** Identifies daily and hourly patterns in pollution.
  - **Anomaly Detection:** Highlights unusual spikes or dips in air quality data.
- **Carbon Footprint Estimator:** Provides a tool to estimate and understand personal carbon emissions.

## 🛠️ Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/CleanAir.git
   cd CleanAir/air_quality_forecast_app
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♀️ Usage

Once the installation is complete, you can run the Streamlit application with the following command:

```bash
streamlit run app.py
```

Navigate to the URL provided by Streamlit in your web browser to access the application.

## 📂 Project Structure

```
Cleanair/
├── air_quality_forecast_app/
│   ├── app.py                # Main Streamlit application
│   ├── requirements.txt      # Python dependencies
│   ├── components/           # UI modules for different features
│   │   ├── anomaly_detection.py
│   │   ├── carbon_footprint_estimator.py
│   │   └── ...
│   ├── model/                # Trained ML models and scalers
│   │   ├── air_quality_model_1h.joblib
│   │   └── ...
│   └── utils/                # Helper functions
│       ├── data_fetching.py
│       └── preprocess.py
└── README.md
```

## 📦 Dependencies

This project relies on the following Python libraries:

- `streamlit`
- `pandas`
- `scikit-learn`
- `joblib`
- `xgboost`
- `lightgbm`
- `plotly`
- `matplotlib`
- `numpy`

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
