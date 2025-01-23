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
        color: #4CAF50;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
        color: #555555;
    }
    .prediction-box {
        background-color: #00CFFF;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
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

# Input form layout
with st.form("laptop_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.selectbox("Company", ['Acer', 'Asus', 'Dell', 'HP', 'Lenovo'])
        typename = st.selectbox("TypeName", ["2 in 1 Convertible", "Notebook", "Gaming"])
        ram = st.selectbox("RAM", ['4GB', '8GB', '12GB', '16GB', '32GB'])
        screen_resolution = st.selectbox("Screen Resolution", ['1366x768', '1920x1080', '2560x1440', '3840x2160'])

    with col2:
        inches = st.number_input("Screen Size (Inches)", min_value=10.0, max_value=20.0, step=0.1)
        memory = st.selectbox("Memory", ["256GB SSD", "512GB SSD", "1.0TB HDD", "2.0TB HDD"])
        weight = st.slider("Weight (KG)", 0.5, 5.0, step=0.1)
        opsys = st.selectbox("Operating System", ["Windows", "MacOS", "Linux", "Android", "Other"])
    
    submitted = st.form_submit_button("Predict")

# Process inputs and make predictions
if submitted:
    # Encode brand as one-hot
    brand_columns = ['Brand_Acer', 'Brand_Asus', 'Brand_Dell', 'Brand_HP', 'Brand_Lenovo']
    brand_input = [0] * len(brand_columns)
    brand_input[brand_columns.index(f'Brand_{brand}')] = 1

    # Combine inputs for prediction
    input_data = np.array([
        float(inches), float(ram.replace("GB", "")), 
        weight, screen_resolution, typename, memory, opsys
    ] + brand_input).reshape(1, -1)
    
    with st.spinner("Calculating price..."):
        prediction = model.predict(input_data)[0]
        
    # Display results
    st.markdown(
        f"""
        <div class="prediction-box">
        Price (Euros): <strong>€{prediction:,.2f}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
