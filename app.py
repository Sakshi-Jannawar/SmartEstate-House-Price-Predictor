import streamlit as st
import pickle
import numpy as np

# Load trained model
model = pickle.load(open("house_model.pkl","rb"))

st.title("🏠 SmartEstate - House Price Predictor")

st.write("Enter house details to predict price")

MedInc = st.number_input("Median Income")
HouseAge = st.number_input("House Age")
AveRooms = st.number_input("Average Rooms")
AveBedrms = st.number_input("Average Bedrooms")
Population = st.number_input("Population")
AveOccup = st.number_input("Average Occupancy")
Latitude = st.number_input("Latitude")
Longitude = st.number_input("Longitude")

if st.button("Predict Price"):

    features = np.array([[MedInc,HouseAge,AveRooms,AveBedrms,
                          Population,AveOccup,Latitude,Longitude]])

    prediction = model.predict(features)

    st.success(f"Estimated House Price: ${prediction[0]*100000:.2f}")