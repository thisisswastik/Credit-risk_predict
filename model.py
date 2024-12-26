import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load('random_forest_model.pkl')  # Or 'svm_model.pkl' if you are using SVM

# Streamlit app title
st.title("Customer Risk Prediction")

# User input fields
st.header("Enter Customer Details:")
age = st.number_input("Age", min_value=18, max_value=120, value=30)
sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: 'Male' if x == 0 else 'Female')
job = st.number_input("Job Type (0-3)", min_value=0, max_value=3, value=0)

# Housing encoding (same as model's training data)
housing = st.selectbox("Housing", options=['No', 'Yes'])

# Saving and Checking Accounts encoding (same as model's training data)
saving_accounts = st.number_input("Saving Accounts (0: None, 1: Little, 2: Moderate, 3: Rich)", min_value=0, max_value=3, value=0)
checking_account = st.number_input("Checking Account (0: None, 1: Little, 2: Moderate, 3: Rich)", min_value=0, max_value=3, value=0)

credit_amount = st.number_input("Credit Amount", min_value=0, value=1000)
duration = st.number_input("Duration (Months)", min_value=1, value=12)

# Purpose selection (same encoding dictionary as used during model training)
purpose = st.selectbox("Purpose", options=[
    'education', 'furniture/equipment', 'radio/TV', 'repairs',
    'domestic appliances', 'car (used)', 'car (new)', 'vacations/others'
])

# One-hot encoding of the 'Purpose' column
purpose_encoding = {
    'education': [1, 0, 0, 0, 0, 0, 0, 0],
    'furniture/equipment': [0, 1, 0, 0, 0, 0, 0, 0],
    'radio/TV': [0, 0, 1, 0, 0, 0, 0, 0],
    'repairs': [0, 0, 0, 1, 0, 0, 0, 0],
    'domestic appliances': [0, 0, 0, 0, 1, 0, 0, 0],
    'car (used)': [0, 0, 0, 0, 0, 1, 0, 0],
    'car (new)': [0, 0, 0, 0, 0, 0, 1, 0],
    'vacations/others': [0, 0, 0, 0, 0, 0, 0, 1],
}


# Ensure the one-hot encoding is consistent with the model's training data
purpose_one_hot = purpose_encoding[purpose]

# One-hot encoding of 'Housing' (No: [1, 0], Yes: [0, 1])
housing_encoding = [1, 0] if housing == 'No' else [0, 1]

# Combine user inputs into a single array (including one-hot encoding for 'Purpose' and 'Housing')
user_input = np.array([[age, sex, job] + housing_encoding + [saving_accounts, checking_account,
                        credit_amount, duration] + purpose_one_hot])

# Check the number of features in the input Predict and display the result
if st.button("Predict"):
    prediction = model.predict(user_input)
    if prediction[0] == 0:
        st.error("The customer is a Bad Risk.")
    else:
        st.success("The customer is a Good Risk.")
