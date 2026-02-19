import streamlit as st
import pickle
import pandas as pd
import os

# ---------------------------
# Load model and scaler
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "rf_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)

# ---------------------------
# App Title
# ---------------------------
st.title("🌍 Tourism Experience Analytics")
st.subheader("Predict Customer Experience Level")

# ---------------------------
# User Inputs
# ---------------------------
user_id = st.number_input("User ID", min_value=1)
item_id = st.number_input("Item ID", min_value=1)
price = st.number_input("Price", min_value=500.0)
quantity = st.number_input("Quantity", min_value=1)
rating = st.number_input("Rating (1-5)", min_value=1, max_value=5)

category = st.selectbox(
    "Category",
    ["Beach", "Adventure", "Heritage", "Wildlife", "Luxury"]
)

# ---------------------------
# Prediction
# ---------------------------
if st.button("Predict Experience Level"):

    input_data = pd.DataFrame({
        "user_id": [user_id],
        "item_id": [item_id],
        "price": [price],
        "quantity": [quantity],
        "rating": [rating],
        "category": [category]
    })

    # One-hot encoding (same as notebook)
    input_data = pd.get_dummies(input_data, columns=["category"], drop_first=True)

    # EXACT training features (must match notebook)
    model_features = [
        "user_id",
        "item_id",
        "price",
        "quantity",
        "rating",
        "category_Beach",
        "category_Heritage",
        "category_Luxury",
        "category_Wildlife"
    ]

    # Add missing columns
    for col in model_features:
        if col not in input_data.columns:
            input_data[col] = 0

    # Reorder correctly
    input_data = input_data[model_features]

    # Scale
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)

    # Convert numeric class to meaningful label
    class_map = {
        0: "Low Experience",
        1: "Medium Experience",
        2: "High Experience"
    }

    predicted_label = class_map.get(prediction[0], "Unknown")

    st.success(f"🎯 Predicted Experience Level: {predicted_label}")

    # Show confidence score
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(input_scaled)
        confidence = round(max(probability[0]) * 100, 2)
        st.info(f"📊 Confidence Level: {confidence}%")
