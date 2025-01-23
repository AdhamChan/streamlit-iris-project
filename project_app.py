import streamlit as st
import joblib
import numpy as np

model = joblib.load('gradient_boosting_model.pkl')

st.title("💻 Ah Lim Laptop Price Predictions 💻")

brand = st.selectbox("Brand", ['Acer', 'Asus', 'Dell', 'HP', 'Lenovo'])
speed = st.slider("Processor Speed (GHz)", 1.5, 4.0, step=0.1)
ram = st.slider('RAM (GB)', 4, 32)
storage = st.slider('Storage (GB)', 256, 1000)
screen_size = st.slider('Screen Size (In)', 11, 17)
weight = st.slider('Weight (KG)', 2, 5)

brand_columns = ['Brand_Acer', 'Brand_Asus', 'Brand_Dell', 'Brand_HP', 'Brand_Lenovo']

brand_input = [0] * len(brand_columns)

brand_input[brand_columns.index(f'Brand_{brand}')] = 1

input_data = np.array([ram, storage, weight, speed, screen_size] + brand_input).reshape(1, -1)

if st.button("Predict"):
    st.write(f"Input Data: {input_data}")  # Print the input data
    prediction = model.predict(input_data)
    st.write(f"Predicted Price: ${prediction[0]:,.2f}")