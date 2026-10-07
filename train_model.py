import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error
import pickle
import os

print("Starting Indian Real Estate Dataset synthesis and Model Training...")

# Seed for reproducibility
np.random.seed(42)

# City & Locality Configurations with coordinates & base price per sqft (in INR)
CITY_CONFIG = {
    "Mumbai": {
        "lat": 19.0760, "lon": 72.8777,
        "localities": {
            "South Mumbai (Colaba/Worli)": {"tier": "Ultra Luxury", "base_sqft": 38000, "lat_off": 0.05, "lon_off": -0.05},
            "Bandra-Juhu Belt": {"tier": "Ultra Luxury", "base_sqft": 32000, "lat_off": 0.08, "lon_off": -0.04},
            "Powai-Andheri West": {"tier": "Premium", "base_sqft": 21000, "lat_off": 0.12, "lon_off": -0.02},
            "Thane West": {"tier": "Mid-Segment", "base_sqft": 13500, "lat_off": 0.20, "lon_off": 0.08},
            "Navi Mumbai (Vashi/Kharghar)": {"tier": "Mid-Segment", "base_sqft": 11000, "lat_off": 0.03, "lon_off": 0.15},
        }
    },
    "Bengaluru": {
        "lat": 12.9716, "lon": 77.5946,
        "localities": {
            "Indiranagar & Koramangala": {"tier": "Ultra Luxury", "base_sqft": 16500, "lat_off": 0.01, "lon_off": 0.04},
            "HSR Layout & Sarjapur": {"tier": "Premium", "base_sqft": 11500, "lat_off": -0.06, "lon_off": 0.06},
            "Whitefield (IT Hub)": {"tier": "Premium", "base_sqft": 9500, "lat_off": 0.01, "lon_off": 0.14},
            "Electronic City": {"tier": "Mid-Segment", "base_sqft": 6500, "lat_off": -0.12, "lon_off": 0.08},
            "Yelahanka & North Blr": {"tier": "Mid-Segment", "base_sqft": 7200, "lat_off": 0.13, "lon_off": -0.01},
        }
    },
    "Delhi NCR": {
        "lat": 28.6139, "lon": 77.2090,
        "localities": {
            "Golf Course Rd (Gurugram)": {"tier": "Ultra Luxury", "base_sqft": 24000, "lat_off": -0.16, "lon_off": -0.11},
            "South Delhi (Vasant Vihar)": {"tier": "Ultra Luxury", "base_sqft": 28000, "lat_off": -0.05, "lon_off": -0.05},
            "Cyber City & Sector 54": {"tier": "Premium", "base_sqft": 15500, "lat_off": -0.14, "lon_off": -0.10},
            "Noida Sector 150/62": {"tier": "Mid-Segment", "base_sqft": 8200, "lat_off": -0.04, "lon_off": 0.17},
            "Greater Noida West": {"tier": "Affordable", "base_sqft": 5400, "lat_off": -0.08, "lon_off": 0.25},
        }
    },
    "Pune": {
        "lat": 18.5204, "lon": 73.8567,
        "localities": {
            "Koregaon Park & Kalyani Nagar": {"tier": "Ultra Luxury", "base_sqft": 14500, "lat_off": 0.02, "lon_off": 0.04},
            "Baner & Balewadi": {"tier": "Premium", "base_sqft": 10200, "lat_off": 0.04, "lon_off": -0.07},
            "Kharadi & Viman Nagar": {"tier": "Premium", "base_sqft": 9200, "lat_off": 0.03, "lon_off": 0.07},
            "Wakad & Hinjewadi": {"tier": "Mid-Segment", "base_sqft": 7400, "lat_off": 0.07, "lon_off": -0.10},
            "Hadapsar & Undri": {"tier": "Mid-Segment", "base_sqft": 6200, "lat_off": -0.04, "lon_off": 0.08},
        }
    },
    "Hyderabad": {
        "lat": 17.3850, "lon": 78.4867,
        "localities": {
            "Jubilee Hills & Banjara Hills": {"tier": "Ultra Luxury", "base_sqft": 16000, "lat_off": 0.05, "lon_off": -0.06},
            "Gachibowli & Financial District": {"tier": "Premium", "base_sqft": 10800, "lat_off": 0.06, "lon_off": -0.12},
            "Kondapur & HITECH City": {"tier": "Premium", "base_sqft": 9800, "lat_off": 0.07, "lon_off": -0.10},
            "Tellapur & Nallagandla": {"tier": "Mid-Segment", "base_sqft": 7500, "lat_off": 0.08, "lon_off": -0.16},
            "Miyapur & Kukatpally": {"tier": "Mid-Segment", "base_sqft": 6100, "lat_off": 0.11, "lon_off": -0.10},
        }
    },
    "Chennai": {
        "lat": 13.0827, "lon": 80.2707,
        "localities": {
            "Adyar & Boat Club Area": {"tier": "Ultra Luxury", "base_sqft": 15000, "lat_off": -0.08, "lon_off": -0.02},
            "Anna Nagar": {"tier": "Premium", "base_sqft": 11500, "lat_off": 0.01, "lon_off": -0.06},
            "OMR IT Corridor (Perungudi)": {"tier": "Mid-Segment", "base_sqft": 7800, "lat_off": -0.12, "lon_off": 0.01},
            "Velachery": {"tier": "Mid-Segment", "base_sqft": 7200, "lat_off": -0.10, "lon_off": -0.04},
            "Tambaram & Porur": {"tier": "Affordable", "base_sqft": 5200, "lat_off": -0.16, "lon_off": -0.12},
        }
    }
}

# Generate 6,000 realistic sample listings
n_samples = 6000
data = []

cities = list(CITY_CONFIG.keys())

for _ in range(n_samples):
    city = np.random.choice(cities)
    c_info = CITY_CONFIG[city]
    locality = np.random.choice(list(c_info["localities"].keys()))
    l_info = c_info["localities"][locality]
    
    bhk = np.random.choice([1, 2, 3, 4, 5], p=[0.15, 0.42, 0.30, 0.10, 0.03])
    
    # Area based on BHK with realistic distribution
    bhk_area_base = {1: (450, 650), 2: (850, 1250), 3: (1350, 1950), 4: (2100, 3200), 5: (3300, 4800)}
    a_min, a_max = bhk_area_base[bhk]
    area = int(np.random.uniform(a_min, a_max))
    
    bathrooms = min(bhk + np.random.choice([0, 1]), 6)
    if bhk == 1: bathrooms = 1
    balconies = np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.3, 0.4, 0.15, 0.05])
    
    prop_age = int(np.random.choice([0, 2, 5, 8, 12, 18, 25], p=[0.25, 0.20, 0.20, 0.15, 0.10, 0.07, 0.03]))
    furnishing = np.random.choice(["Unfurnished", "Semi-Furnished", "Fully-Furnished"], p=[0.35, 0.45, 0.20])
    floor_level = np.random.choice(["Ground-Low (1-4)", "Mid (5-12)", "High (13+)"], p=[0.40, 0.40, 0.20])
    amenities_score = int(np.random.choice(range(1, 11)))
    
    # Pricing formula with noise
    base_sqft = l_info["base_sqft"]
    
    # Adjustments
    furnish_mult = {"Unfurnished": 1.0, "Semi-Furnished": 1.06, "Fully-Furnished": 1.14}[furnishing]
    floor_mult = {"Ground-Low (1-4)": 1.0, "Mid (5-12)": 1.04, "High (13+)": 1.09}[floor_level]
    age_mult = max(0.72, 1.0 - (prop_age * 0.012))
    amenity_mult = 1.0 + (amenities_score * 0.015)
    
    # Random market noise (+/- 7%)
    noise = np.random.normal(1.0, 0.05)
    
    price_per_sqft = base_sqft * furnish_mult * floor_mult * age_mult * amenity_mult * noise
    total_price_inr = price_per_sqft * area
    
    # Price in Lakhs (1 Lakh = 100,000 INR)
    price_lakhs = round(total_price_inr / 100000.0, 2)
    
    # Add coordinate with slight jitter
    lat = c_info["lat"] + l_info["lat_off"] + np.random.uniform(-0.01, 0.01)
    lon = c_info["lon"] + l_info["lon_off"] + np.random.uniform(-0.01, 0.01)
    
    data.append({
        "City": city,
        "Locality": locality,
        "Locality_Tier": l_info["tier"],
        "BHK": bhk,
        "Area_SqFt": area,
        "Bathrooms": bathrooms,
        "Balconies": balconies,
        "Property_Age": prop_age,
        "Furnishing": furnishing,
        "Floor_Level": floor_level,
        "Amenities_Score": amenities_score,
        "Latitude": round(lat, 5),
        "Longitude": round(lon, 5),
        "Price_Lakhs": price_lakhs
    })

df = pd.DataFrame(data)

# Save dataset to CSV for exploration
df.to_csv("indian_housing_data.csv", index=False)
print(f"Dataset generated and saved to indian_housing_data.csv with {len(df)} records.")

# Prepare X and y
X = df.drop(columns=["Price_Lakhs"])
y = df["Price_Lakhs"]

categorical_features = ["City", "Locality", "Locality_Tier", "Furnishing", "Floor_Level"]
numerical_features = ["BHK", "Area_SqFt", "Bathrooms", "Balconies", "Property_Age", "Amenities_Score", "Latitude", "Longitude"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ("num", StandardScaler(), numerical_features)
    ]
)

rf = RandomForestRegressor(n_estimators=120, max_depth=16, random_state=42, n_jobs=-1)
gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.08, max_depth=6, random_state=42)

ensemble_model = VotingRegressor(estimators=[("rf", rf), ("gb", gb)])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", ensemble_model)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

print(f"Model Performance:")
print(f"  R² Score: {r2:.4f}")
print(f"  MAE: ₹{mae:.2f} Lakhs")
print(f"  RMSE: ₹{rmse:.2f} Lakhs")

# Package model and metadata into pickle
model_pack = {
    "pipeline": pipeline,
    "city_config": CITY_CONFIG,
    "metrics": {
        "r2": round(r2, 4),
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "samples": len(df)
    },
    "features": list(X.columns)
}

with open("house_model.pkl", "wb") as f:
    pickle.dump(model_pack, f)

print("Indian House Price Model trained and saved to house_model.pkl successfully!")