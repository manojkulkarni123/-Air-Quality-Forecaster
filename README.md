# 🌍 Air Quality Forecaster

An end-to-end **Machine Learning web application** that forecasts **PM2.5 air pollution levels and AQI** up to 24 hours ahead, with population-specific health advisories.

> Built as part of an Urban Air Quality Forecasting and Health Advisory System assignment (End-to-End ML Experimental Design).

🔗 **GitHub:** [manojkulkarni123/-Air-Quality-Forecaster](https://github.com/manojkulkarni123/-Air-Quality-Forecaster)

---

## 📌 Overview

This project forecasts future air pollution using trained Random Forest models on Beijing hourly air quality data (2013–2017). Unlike a standard predictor, this system is designed as a genuine **forecaster** — it predicts PM2.5 concentrations at future time horizons using historical lag features, and converts those predictions into true EPA AQI scores with tailored health guidance per population group.

---

## 🚀 Key Features

### Multi-Horizon Forecasting
Three separate models predict PM2.5 at different time horizons — 1 hour, 6 hours, and 24 hours ahead. All three forecasts are shown simultaneously in a comparison table so users can see whether air quality is improving or deteriorating over the day.

### True EPA AQI Conversion
Raw PM2.5 µg/m³ values are converted to AQI using the official EPA piecewise linear formula — not a simplified threshold check. This means a PM2.5 of 55 µg/m³ correctly returns AQI 151 (Unhealthy) rather than being misclassified as Moderate.

### Population-Specific Health Advisory
A 6 × 5 advisory matrix covers six AQI categories across five population groups: General Public, Elderly, Children, Respiratory, and Cardiovascular. Each combination returns distinct, medically appropriate guidance.

### Lag & Rolling Features
The model uses recent PM2.5 history as its strongest predictive signal:
- `PM2.5_lag1` — reading from 1 hour ago
- `PM2.5_lag3` — reading from 3 hours ago
- `PM2.5_rolling6h` — 6-hour rolling average
- `PM2.5_rolling24h` — 24-hour rolling average

### Preprocessing and train/test split
- Chronological 80/20 train/test split — no random shuffling
- Sparse columns (>50% missing) dropped; remaining gaps filled with forward-fill

### Consistent Deployment Encodings
Season and wind direction label encodings are saved to `.pkl` files during training and loaded by the app, ensuring the app uses the exact same mappings as the model.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| ML Models | Random Forest (scikit-learn) |
| Data Processing | pandas, numpy |
| Model Persistence | joblib |
| Dataset | Beijing Air Quality 2013–2017 |

---

## 📥 Input Parameters

| Input | Description |
|---|---|
| Current PM2.5 (µg/m³) | Most recent reading — drives all lag features |
| Temperature (°C) | Ambient temperature |
| Pressure (hPa) | Atmospheric pressure |
| Wind Speed (m/s) | Surface wind speed |
| Wind Direction | Compass direction (from training vocabulary) |
| Season | Autumn / Spring / Summer / Winter |
| Hour / Day / Month | Time context for prediction |
| Forecast Horizon | 1h, 6h, or 24h ahead |
| Population Group | General / Elderly / Children / Respiratory / Cardiovascular |
| Advanced (optional) | PM10, SO2, NO2, CO, O3, Dew Point, Precipitation |

---

## 📤 Output

- Predicted **PM2.5 (µg/m³)** and **AQI** for the chosen horizon
- Current vs forecast AQI with delta indicator (rising/falling)
- Colour-coded AQI band (Green → Maroon)
- Health advisory tailored to the selected population group
- Comparison table across all 3 horizons with per-horizon advisory

---

## 🧠 ML Pipeline

### Problem Formulation
Regression task: predict PM2.5 concentration N hours into the future given current meteorological and pollutant conditions plus recent PM2.5 history.

### Data Preprocessing

| Issue | Fix Applied |
|---|---|
| Leaky station columns | Dropped `PM_Station 1/2/3`, `PM_US Post` |
| Random train/test split | Chronological 80/20 split |
| Sparse columns (>50% missing) | Dropped entirely |
| Remaining missing values | Forward-fill (time-series appropriate) |
| Duplicate/redundant columns | Dropped Fahrenheit duplicates, duplicate PM2.5 column |

### Feature Engineering

- **Lag features:** `PM2.5_lag1`, `PM2.5_lag3`, `PM2.5_rolling6h`, `PM2.5_rolling24h`
- **Temporal features:** `hour`, `day`, `month`, `dayofweek`
- **Categorical encoding:** `Season`, `Wind Direction` — saved to `.pkl` for deployment
- **AQI computation:** EPA piecewise linear formula applied to target

### Models

| File | Horizon | Description |
|---|---|---|
| `air_quality_model_t1.pkl` | +1 hour | Short-term forecast |
| `air_quality_model_t6.pkl` | +6 hours | Medium-term forecast |
| `air_quality_model_t24.pkl` | +24 hours | Day-ahead forecast |

Each model: `RandomForestRegressor(n_estimators=50, max_depth=20, max_samples=100_000)`

### Evaluation
Models are evaluated on the chronological test set (last 20% of data) using MAE, RMSE, and R².

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/manojkulkarni123/-Air-Quality-Forecaster.git
cd -Air-Quality-Forecaster
```

### 2. Install dependencies

```bash
pip install pandas numpy scikit-learn joblib streamlit matplotlib
```

### 3. Add the dataset

Extract `Beijing Air Quality from 2010 to 2017.zip` and place the `.csv` in the project root.

### 4. Train the models

Run all cells in `air_quality_model.ipynb` top to bottom. This generates all `.pkl` files.

### 5. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
Air-Quality-Forecaster/
│
├── app.py                          # Streamlit web app
├── air_quality_model.ipynb         # Full ML pipeline (7 steps)
│
├── air_quality_model_t1.pkl        # Trained model: +1h forecast
├── air_quality_model_t6.pkl        # Trained model: +6h forecast
├── air_quality_model_t24.pkl       # Trained model: +24h forecast
│
├── features.pkl                    # Feature column order (for inference)
├── season_encoding.pkl             # Season → integer mapping
├── wind_direction_encoding.pkl     # Wind direction → integer mapping
│
├── feature_importance.png          # Top-10 feature importance per horizon
│
├── Beijing Air Quality from 2010 to 2017.zip   # Dataset (zipped)
├── .gitignore
└── README.md
```

---

## 🎯 Use Cases

- Urban air quality monitoring
- Public health advisory systems
- Smart city environmental dashboards
- Academic ML assignment — End-to-End Experimental Design

---

## 📄 License

This project is for educational purposes.

---

⭐ If you found this useful, give it a star!
