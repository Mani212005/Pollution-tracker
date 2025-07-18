#  spec.md — Serverless AI-Based Real-Time Air Pollution Forecasting App (Delhi)

##  Project Title:

**Delhi Air Pollution Forecasting and Alert System (Serverless Edition)**

##  Goal

Build a serverless, deployable application using **Streamlit** that:

* Collects real-time air pollution and weather data.
* Forecasts PM2.5 and AQI using a trained ML model.
* Provides real-time health alerts and visualizations.
* Is self-contained with no separate backend server (no FastAPI or Flask).

---

## ✅ Key Features

| Feature               | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| Real-Time Prediction  | Forecast PM2.5 / AQI for 1-hour ahead using trained ML model             |
| Interactive Dashboard | Streamlit-based UI with maps, charts, and metrics                        |
| Instant Alerts        | Health warnings triggered by forecast thresholds                         |
| Model Integration     | ML model and scaler are loaded directly into memory with no external API |
| One-Click Deployment  | Easily deployed on Streamlit Community Cloud or any Python environment   |

---

##  System Architecture (Serverless)

```plaintext
User Opens App
    └──> Streamlit App Starts
            ├──> Load Model + Scaler (joblib)
            ├──> Fetch Real-Time Data (APIs / DB)
            ├──> Preprocess + Feature Engineering
            ├──> Predict Air Quality
            └──> Render Charts, Maps, Alerts
```

---

## ️ Project Structure

```
air_quality_forecast_app/
│
├── app.py                       # Main Streamlit dashboard
├── model/
│   ├── train_model.py          # Training script (XGBoost/LightGBM)
│   ├── air_quality_model.joblib
│   └── data_scaler.joblib
├── utils/
│   ├── data_fetching.py        # Fetches data from APIs or DB
│   └── preprocess.py           # Cleans + engineers features
├── components/
│   ├── map_view.py             # Streamlit AQI map
│   ├── time_series_plot.py     # Trend plots
│   └── health_alerts.py        # Advisory logic
├── requirements.txt
└── spec.md
```

---

##  Model Development

### ✅ Step 1: Train Model

* Algorithm: XGBoost / LightGBM
* Target: PM2.5 (next 1-hour)
* Inputs: Historical pollution, weather, time features
* Tools: Scikit-learn, Pandas, Joblib

### ✅ Step 2: Evaluate Model

* Metrics: RMSE, MAE
* Visualization: Predicted vs Actual

### ✅ Step 3: Serialize Assets

```python
import joblib
joblib.dump(model, 'air_quality_model.joblib')
joblib.dump(scaler, 'data_scaler.joblib')
```

---

## ⚙️ Streamlit Integration

### ✅ Load Model in App

```python
 @st.cache_resource
def load_model():
    model = joblib.load('model/air_quality_model.joblib')
    scaler = joblib.load('model/data_scaler.joblib')
    return model, scaler
```

### ✅ Predict on New Data

```python
def run_prediction(raw_data_df):
    processed_df = preprocess(raw_data_df)
    scaled = scaler.transform(processed_df)
    forecast = model.predict(scaled)
    return forecast
```

---

##  UI Components

| Component    | Function                                     |
| ------------ | -------------------------------------------- |
| Title Header | App name, city selection                     |
| Map View     | Live AQI readings on map (Mapbox / Plotly)   |
| Trend Plot   | PM2.5 and AQI time series                    |
| Metrics Card | Forecasted PM2.5, health risk level          |
| Alert Box    | Condition-based warnings (AQI > 300 = alert) |

---

##  Alerting Logic

```python
if predicted_pm25 > 300:
    st.error("HEALTH ALERT: Severe air quality forecast. Avoid outdoor activity.")
elif predicted_pm25 > 200:
    st.warning("Unhealthy air quality forecast. Sensitive groups be cautious.")
else:
    st.success("Air quality looks acceptable.")
```

---

##  Data Sources

* **CPCB** or **WAQI** API for PM2.5, PM10, AQI
* **OpenWeatherMap** for wind, temperature, humidity
* **Optional:** Google Maps API for traffic index

---

##  Storage (Optional for Streamlit Cloud)

* PostgreSQL + TimescaleDB (for long-term storage)
* Or store snapshots in CSV/Parquet for lightweight apps

---

##  Tech Stack Summary

| Layer              | Tools                              |
| ------------------ | ---------------------------------- |
| ML & Preprocessing | XGBoost, scikit-learn, joblib      |
| App Framework      | Streamlit                          |
| Visualization      | Plotly, Streamlit Maps             |
| Data Sources       | WAQI API, OpenWeatherMap API       |
| Deployment         | Streamlit Community Cloud / Docker |

---

##  Deployment Options

### ✅ Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

### ✅ Streamlit Cloud

* Push to GitHub
* Deploy via: [https://streamlit.io/cloud](https://streamlit.io/cloud)

### ✅ Docker (Optional)

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
```

---

##  Deliverables Checklist

| Task                  | Deliverable                                 |
| --------------------- | ------------------------------------------- |
| ✅ Model Training      | `air_quality_model.joblib`, `scaler.joblib` |
| ✅ Streamlit Dashboard | `app.py`, UI components                     |
| ✅ Alert Logic         | In-dashboard warnings                       |
| ✅ Realtime Prediction | Single function pipeline                    |
| ✅ Deployment          | Streamlit Cloud or Docker                   |
| ✅ Documentation       | `spec.md`, `README.md`, inline comments     |
