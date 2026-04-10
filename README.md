# 📺 DOOH Expected Plays Calculator

A clean and interactive Streamlit app to **estimate expected ad plays** across Digital Out-of-Home (DOOH) screens based on campaign schedule, screen availability, loop structure, and Share of Voice.

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





Where:

- **Loop Duration** → Total ad cycle time in seconds
- **Slot Duration** → Length of one ad slot within the loop
- **SOV (%)** → Share of Voice — the % of loop slots your ad occupies; used to calculate how many slots are allocated via `CEIL(Total Slots × SOV%)`
- **Overlap Hours** → Intersection of campaign schedule and screen operating hours
- **Units** → Number of physical screens at the location

> **Example:** A 60s loop with 10s slots = 6 total slots. At 33% SOV → `CEIL(6 × 0.33) = 2` slots allocated. At 60 loops/hr → **120 plays/hour per unit.**

---

## 📂 Input Requirements

Upload an Excel file containing the following required columns:

| Column | Description |
|:---|:---|
| `Units` | Number of physical screen panels at the location |
| `Loop Duration (Sec)` | Total length of one content loop in seconds |
| `Slot Duration (Sec)` | Length of one ad slot within the loop |
| `SOV (%)` | Share of Voice — % of loop slots allocated to this ad |
| `Operating Hours` | Screen-on window in `HH:MM-HH:MM` format (e.g. `06:00-23:00`) |

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

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run expected_adplays.py
```

## 🌐 Live App

👉 https://dooh-expected-plays.streamlit.app

---

## 📌 Use Case

Ideal for:
- Media planners
- DOOH campaign managers
- Ad operations teams

---

## ✨ Author

**Shubham Raut**
Data & Analytics | DOOH | Automation
