# 🧠 Real-Time Seizure Detection using Smartphone Sensors  

This project is a **machine learning–powered application** designed to help monitor patients who frequently experience hand seizures. Using a smartphone’s built-in **accelerometer** and **gyroscope**, the system captures real-time motion data, learns movement patterns, and detects whether the patient is in a **normal** or **seizure** state.  

---

## 🚀 Features  

### 📱 Sensor Data Collection  
- Captures accelerometer (**x, y, z**) and gyroscope (**gx, gy, gz**) readings directly from an Android device via **ADB**.  

### 🔎 Seizure Detection Model  
- Trains a **Random Forest classifier** on labeled movement data (`normal.json` and `seizure.json`) to recognize seizure-like hand movements.  

### ⚡ Live Monitoring with UI  
A **Tkinter-based desktop application** provides real-time monitoring with:  
- ▶️ Start / Stop live detection  
- 📚 Train model button  
- Visual feedback: 🟢 **Normal** or 🔴 **Seizure detected**  

### 💾 Data Logging  
- Automatically stores sensor readings into JSON files for training, testing, and future analysis.  

---

## 🛠 Tech Stack  
- 🐍 **Python** (Data processing, ML, UI)  
- 🌲 **Scikit-learn** (RandomForest classifier)  
- 🔢 **NumPy** (Feature extraction)  
- 🎨 **Tkinter** (User interface)  
- 📡 **Ndroid Debugging Bridge - ADB** (Sensor data streaming from Android device)  

---

## 📂 Project Structure  
- `appui.py` → Live monitoring UI  
- `parse.py` → Generates json file from accelerometer feed 
- `seiz.py` → Training script for the seizure detection model  
- `sz2.py` → Testing detection with per-generated json data
-  `update.py` → Testing with live detection scripts  
- `norm_real.json` / `seiz_real.json` → Sample training data
- `real_model.pkl` → Trained model data

---

## 🔬 Future Improvements  
- 🤖 Integrate **deep learning (LSTM/1D-CNN)** to capture time-series seizure patterns  
- 📊 Collect and process **larger datasets** for higher accuracy  
- 🎵 Add **frequency-domain features** for better movement classification  
- 📱 Deploy as a **mobile app** for patient-side monitoring  

---

## ⚠️ Disclaimer  
This project is a **research and experimental tool**, not a certified medical device.  
It should **not** be used for clinical diagnosis or treatment decisions.  
