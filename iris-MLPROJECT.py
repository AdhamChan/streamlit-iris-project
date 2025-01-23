import streamlit as st
import joblib
import numpy as np

# Load the model
model = joblib.load('gradient_boosting.pkl')

# App title with styling
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
        color: white;
    }
    # .st-emotion-cache-bm2z3a {
    #     background-color: black
    # }

    </style>
    <div class="title">Laptop Price Predictions</div>
    <div class="subtitle">Enter the laptop specifications below to predict the price</div>
    """,
    unsafe_allow_html=True
)

# User Input section
def user_inputs():
    st.sidebar.header("🔧 Input Specifications")
    brand = st.sidebar.selectbox("Brand", ['Acer', 'Asus', 'Dell', 'HP', 'Lenovo'])
    speed = st.sidebar.slider("Processor Speed (GHz)", 1.5, 4.0, step=0.1)
    ram = st.sidebar.slider('RAM (GB)', 4, 32)
    storage = st.sidebar.slider('Storage (GB)', 256, 1000)
    screen_size = st.sidebar.slider('Screen Size (In)', 11, 17)
    weight = st.sidebar.slider('Weight (KG)', 2, 5)
    return brand, speed, ram, storage, screen_size, weight

brand, speed, ram, storage, screen_size, weight = user_inputs()

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

# Prediction section
if st.button("💻 Predict Price 💻"):
    with st.spinner("Calculating price..."):
        prediction = model.predict(input_data)
        st.success(f"The predicted price for the laptop is: ** ₽{prediction[0]:,.2f}**")
