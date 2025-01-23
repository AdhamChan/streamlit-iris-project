import streamlit as st
import joblib
import numpy as np

# Load the model
model = joblib.load('gradient_boosting.pkl')

# App title and styling
st.markdown(
    """
    <style>

    .title {
        font-size: 36px;
        font-weight: bold;
        color: pink;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
    }
    .prediction-box {
        background-color: #00CFFF;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 20px;
        margin-top: 20px;
    }
    .predict-btn {
        background-color: #007BFF;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .predict-btn:hover {
        background-color: #0056b3;
    }
    </style>
    <div class="title">Laptop Price Predictions</div>
    <div class="subtitle">Enter the laptop specifications below to predict the price</div>
    """,
    unsafe_allow_html=True,
)

# Input section layout
st.markdown("### Enter Laptop Specifications ###")
col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("Brand", ['Acer', 'Asus', 'Dell', 'HP', 'Lenovo'])
    speed = st.slider("Processor Speed (GHz)", 1.5, 4.0, step=0.1)
    ram = st.slider("RAM (GB)", 4, 32)

with col2:
    storage = st.slider("Storage (GB)", 256, 1000)
    screen_size = st.slider("Screen Size (In)", 11, 17)
    weight = st.slider("Weight (KG)", 2, 5)

# Encode brand as one-hot
brand_columns = ['Brand_Acer', 'Brand_Asus', 'Brand_Dell', 'Brand_HP', 'Brand_Lenovo']
brand_input = [0] * len(brand_columns)
brand_input[brand_columns.index(f'Brand_{brand}')] = 1

# Combine inputs
input_data = np.array([speed, ram, storage, screen_size, weight] + brand_input).reshape(1, -1)

# Display input data summary
st.markdown("### Your Laptop Specifications ###")
st.table({
    "Specification": ["Brand", "Processor Speed (GHz)", "RAM (GB)", "Storage (GB)", "Screen Size (In)", "Weight (KG)"],
    "Value": [brand, speed, ram, storage, screen_size, weight]
})

# Prediction button and result display
if st.button("💻 Predict Price 💻"):
    with st.spinner("Calculating price..."):
        prediction = model.predict(input_data)
    st.markdown(
        f"""
        <div class="prediction-box">
        Predicted Price: <strong>€{prediction[0]:,.2f}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
