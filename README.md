# CleanAir: AI-Powered Air Quality Forecasting & Health Advisory System

CleanAir is a comprehensive web application built with Streamlit that provides real-time air quality forecasting, health alerts, and insightful visualizations. Leveraging machine learning, this tool empowers users to stay informed about air pollution levels and make data-driven decisions for their health and well-being.

![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu1.png)

## 🚀 Features

 🔄 **Real-time Data Integration**  
  Fetches live air quality and weather data from global monitoring sources.

- ⏱️ **Multi-Horizon Forecasting**  
  Predicts PM2.5 levels for 1, 3, 6, and 12 hours using ML models.

- 🧮 **Dynamic AQI Calculation**  
  Converts PM2.5 into easy-to-understand Air Quality Index (AQI) levels.

- ⚕️ **Automated Health Alerts**  
  Sends health recommendations based on forecasted AQI.

- 🗺️ **Interactive Map View**  
  Visualizes air quality for user-selected cities on an interactive map.

- 📊 **Insightful Visualizations**  
  - Time-series analysis of historical and forecasted AQI  
  - Feature importance using ML model interpretability  
  - Temporal heatmaps for hourly/daily trends  
  - Anomaly detection for sudden pollution spikes

- 🌱 **Carbon Footprint Estimator**  
  Estimate your individual emissions and get actionable insights.

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
- `scikit-learn` (for RandomForestRegressor)
- `lightgbm`
- `plotly`
- `matplotlib`
- `numpy`

![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu11.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu3.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu4.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu5.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu6.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu7.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu8.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu9.png)
![Image_Alt](https://github.com/Mani212005/Pollution-tracker/blob/d864e09f30ceb975ffa0f9380cad29828e642160/pollu10.png)
 

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
