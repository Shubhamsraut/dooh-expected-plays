# 📺 DOOH Expected Plays Calculator

A clean and interactive Streamlit app to **estimate expected ad plays** across Digital Out-of-Home (DOOH) screens based on campaign schedule, screen availability, and loop duration.

---

## 🚀 What this app does

- 📅 Define campaign duration and hourly schedule
- 📊 Upload screen inventory (Excel)
- ⚙️ Automatically calculate expected plays per screen
- 📈 View sorted results with key metrics
- 🔍 Drill down into a detailed calculation breakdown
- ⬇️ Export results to Excel

---

## 🧠 How it works

Expected Plays are calculated using:
Expected Plays = (3600 / Loop Duration) × Overlap Hours × Units


Where:
- **Loop Duration** → Ad cycle time (seconds)
- **Overlap Hours** → Campaign schedule ∩ Screen operating hours
- **Units** → Number of screens at location

---

## 📂 Input Requirements

Upload an Excel file containing the following required columns:

- **Units** → Number of screens at the location  
- **Loop Duration (Sec)** → Ad loop duration in seconds  
- **Operating Hours** → Screen active hours (format: `HH:MM-HH:MM`, e.g., `08:00-22:00`)

⚠️ **Note:**
- Column names must match exactly as above  
- Column order/position does **not matter**  
- Additional columns are allowed and will be preserved in the output

---


## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas

---

# 📺 DOOH Expected Plays Calculator

A clean and interactive Streamlit app to **estimate expected ad plays** across DOOH screens based on campaign schedule and screen availability.

---

## 🚀 Run Locally

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run expected_adplays.py
```

## 🌐 Live App

👉 https://dooh-expected-plays.streamlit.app

## 📌 Use Case

### Ideal for:
- Media planners
- DOOH campaign managers
- Ad operations teams

## ✨ Author

**Shubham Raut**  
Data & Analytics | DOOH | Automation




