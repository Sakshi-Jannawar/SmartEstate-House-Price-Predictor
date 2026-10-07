# 🏙️ SmartEstate — House Price Predictor & Real Estate Analytics Platform

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

SmartEstate is an advanced ML-driven Real Estate Valuation & Market Intelligence Platform designed for major Indian metropolitan cities including **Mumbai**, **Bengaluru**, **Delhi NCR**, **Pune**, **Hyderabad**, and **Chennai**.

---

## 🌟 Key Features

### 🎯 1. ML Valuation Engine
- **Ensemble Machine Learning Architecture**: Combines `RandomForestRegressor` and `GradientBoostingRegressor` via a `VotingRegressor` for robust pricing estimates ($R^2 \approx 0.98$).
- **Multi-Factor Real Estate Inputs**: Supports City, Locality, Locality Tier (Ultra-Luxury, Premium, Mid-Segment, Affordable), BHK configuration, Square Footage, Bathrooms, Balconies, Property Age, Furnishing status, Floor level, Amenities score, and Geolocation coordinates.
- **Dynamic Valuation Range**: Instant estimated property value (Lakhs & Crores INR) with expected confidence bounds.

### 🧠 2. Explainable AI (XAI) Feature Attribution
- **Mathematical Price Decomposition**: Breaks down exactly how each property attribute (Location, Area, BHK, Amenities, Age, Floor Level, etc.) adds or subtracts value relative to the base market rate.
- **Waterfall & Bar Impact Charts**: Interactive Plotly visualizations explaining model decisions transparently.

### 📊 3. Metropolitan Market Intelligence
- **Cross-City Market Comparison**: Compare property price metrics across Mumbai, Bengaluru, Delhi NCR, Pune, Hyderabad, and Chennai.
- **Interactive Price Distribution & Heatmaps**: Explore property trends by locality tier, BHK configuration, and price per sq. ft.
- **Geographic Mapping**: Interactive geospatial scatter plots powered by Plotly.

### 💼 4. Investment & Mortgage Calculator
- **Mortgage EMI Calculation**: Instant monthly EMI calculation based on customizable down payment, interest rates, and loan tenure.
- **Rental Yield & Return Estimation**: Forecast expected monthly rental yield and cap rates.
- **5-Year Capital Appreciation Projection**: Multi-year property value growth scenario modeling.

### 📁 5. Portfolio & Session History
- **Recent Valuations Tracking**: Saves search history during active session for easy comparison.
- **CSV Data Export**: One-click download of valuation reports and dataset.

---

## 📁 Repository Structure

```
SmartEstate-House-Price-Predictor/
│
├── app.py                      # Main Streamlit Dashboard Application
├── train_model.py              # ML Model Training & Synthetic Data Generation Script
├── indian_housing_data.csv     # Synthesized Indian Real Estate Dataset (6,000 records)
├── requirements.txt            # Python Dependencies
├── .gitignore                  # Git Ignore Rules
└── .streamlit/
    └── config.toml             # Streamlit Dark Theme & UI Configuration
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.9+
- `pip` package manager

### 1. Clone the Repository
```bash
git clone https://github.com/Sakshi-Jannawar/SmartEstate-House-Price-Predictor.git
cd SmartEstate-House-Price-Predictor
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model (Optional)
The application automatically checks for `house_model.pkl` and trains the model on launch if absent. To train manually:
```bash
python train_model.py
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🔐 Demo Login Credentials

The platform includes demo credentials for instant testing:

| Email / Username | Password | Role | City |
| :--- | :--- | :--- | :--- |
| `sakshi@smartestate.in` | `pass` | Senior Analyst | Mumbai |
| `admin` | `123` | Real Estate Director | Bengaluru |
| `investor@smartestate.in` | `123` | Property Investor | Delhi NCR |

---

## 🛠️ Tech Stack

- **Frontend & UI**: Streamlit, Custom Glassmorphism CSS, Google Fonts (*Plus Jakarta Sans*, *Space Grotesk*)
- **Data Analytics & Visualizations**: Plotly Express, Plotly Graph Objects, Pandas, NumPy
- **Machine Learning**: Scikit-Learn (`RandomForestRegressor`, `GradientBoostingRegressor`, `VotingRegressor`, `Pipeline`, `ColumnTransformer`)
- **Persistence**: Pickle

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
