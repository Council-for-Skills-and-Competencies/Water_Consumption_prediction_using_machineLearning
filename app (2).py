import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

# Load the custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the trained model
try:
    model = joblib.load('model.joblib')
except FileNotFoundError:
    st.error("Model file 'model.joblib' not found. Please run 'train_and_save_model.py' first.")
    st.stop()

# Get the list of amenities and apartment types used in training
apartment_types = ['Studio', '1BHK', '2BHK', '3BHK', 'Cottage']
income_levels = ['Low', 'Middle', 'Upper Middle', 'High']
amenities = ['Swimming Pool', 'Garden', 'Jacuzzi', 'None']
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Streamlit UI
st.title('🌊 Water Consumption Prediction')
st.markdown("This app predicts water consumption based on household and environmental factors.")

# Sidebar for user input
with st.sidebar:
    st.header('Household & Environmental Factors')

    # Add date/time inputs for Day, Month, Hour, and Day of Week
    st.subheader('Date and Time')
    col1, col2, col3 = st.columns(3)
    with col1:
        month = st.number_input('Month', min_value=1, max_value=12, value=datetime.now().month)
    with col2:
        day = st.number_input('Day', min_value=1, max_value=31, value=datetime.now().day)
    with col3:
        hour = st.number_input('Hour', min_value=0, max_value=23, value=datetime.now().hour)
    day_of_week_str = st.selectbox('Day of Week', days_of_week, index=datetime.now().weekday())
    day_of_week = days_of_week.index(day_of_week_str)

    st.subheader('Usage and Socio-Economic Factors')
    residents = st.slider('Number of Residents', 1, 5, 2)
    apartment_type = st.selectbox('Apartment Type', apartment_types)
    income_level = st.selectbox('Income Level', income_levels)
    amenity = st.selectbox('Amenities', amenities)
    appliance_usage = st.slider('Appliance Usage (0 = Low, 1 = High)', 0, 1, 0)
    
    st.subheader('Environmental Factors')
    temperature = st.number_input('Temperature (°C)', min_value=0.0, max_value=40.0, value=25.0)
    humidity = st.number_input('Humidity (%)', min_value=0.0, max_value=100.0, value=60.0)
    water_price = st.number_input('Water Price (per unit)', min_value=0.0, max_value=10.0, value=1.5)
    period_consumption_index = st.number_input('Period Consumption Index', min_value=0.0, max_value=3.0, value=1.0)
    guests = st.slider('Number of Guests', 0, 5, 0)

# Create a dataframe for the input data
input_data = pd.DataFrame([{
    'Residents': residents,
    'Apartment_Type': apartment_type,
    'Temperature': temperature,
    'Humidity': humidity,
    'Water_Price': water_price,
    'Period_Consumption_Index': period_consumption_index,
    'Income_Level': income_level,
    'Guests': guests,
    'Amenities': amenity,
    'Appliance_Usage': appliance_usage,
    'Day': day,
    'Month': month,
    'Hour': hour,
    'DayofWeek': day_of_week,
}])

# Convert categorical columns to 'category' dtype
input_data['Apartment_Type'] = input_data['Apartment_Type'].astype('category')
input_data['Income_Level'] = input_data['Income_Level'].astype('category')
input_data['Amenities'] = input_data['Amenities'].astype('category')

# Main section for output
st.subheader("Prediction Result")
if st.button('Predict Water Consumption', key="predict_button"):
    try:
        # Make a prediction using the loaded model
        prediction = model.predict(input_data)[0]
        
        # Display the prediction with a success message
        st.success(f"Predicted Water Consumption: **{prediction:.2f}** units")
        st.balloons()
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")