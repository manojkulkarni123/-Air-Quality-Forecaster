# 🌍 Air Quality Predictor

A simple and interactive **Machine Learning web application** that predicts **PM2.5 air pollution levels** based on environmental parameters such as temperature, humidity, pressure, and wind speed.

---

## 📌 Overview

This project helps users estimate air pollution levels in real time using a trained ML model. It provides:

* PM2.5 prediction
* Air Quality status (Good, Moderate, Unhealthy, etc.)
* Precautionary suggestions based on pollution level

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Machine Learning Model:** Random Forest (joblib)
* **Libraries Used:**

  * pandas
  * joblib
  * streamlit

---

## 🚀 Features

* ✅ User-friendly dashboard UI
* ✅ Real-time prediction
* ✅ Air Quality classification
* ✅ Health precautions based on AQI
* ✅ Clean and responsive layout

---

## 📥 Input Parameters

The model takes the following inputs:

* 🌡️ Temperature (°C)
* 💧 Humidity (%)
* 🌬️ Wind Speed (m/s)
* 📊 Pressure (hPa)
* ⏰ Hour of the day

---

## 📤 Output

* 📈 Predicted **PM2.5 value (µg/m³)**
* 🌈 Air Quality Status:

  * Good
  * Moderate
  * Unhealthy (Sensitive)
  * Unhealthy
  * Very Unhealthy
* ⚠️ Suggested precautions

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/air-quality-predictor.git
cd air-quality-predictor
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
Air-Quality-Predictor/
│── app.py
│── air_quality_model.pkl
│── features.pkl
│── requirements.txt
│── README.md
```

---

## 🧠 How It Works

1. User enters environmental parameters
2. Input data is preprocessed and aligned with model features
3. Trained ML model predicts PM2.5 value
4. Result is displayed along with AQI category and precautions

---

## 🎯 Use Cases

* Environmental monitoring
* Academic projects
* Awareness of air pollution levels
* Smart city applications

---

## 📬 Contact

* 📧 Email: pradeepg.cs24@bmsce.ac.in
* 🌐 GitHub: [https://github.com/yourusername](https://github.com/Pradeepg06/air_quality_ml_model.git)

---

## 📄 License

This project is for educational purposes.

---

⭐ If you like this project, consider giving it a star!
