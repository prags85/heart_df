import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_model = joblib.load('heart_prediction.pkl')

# Function to predict values
def predict_values():
    st.write('You will be needing to enter the following 10 values for best results: ')
    trestbps = st.number_input('Enter resting Blood Pressure: ')
    oldpeak = st.number_input('Enter ST depression induced by exercise relative to rest (decimal): ')
    sex = st.selectbox('Select gender:', ['male', 'female'])
    cp = st.selectbox('Select type of Chest Pain:', ['atypical angina', 'typical angina', 'non-anginal', 'asymptomatic'])
    fbs = st.number_input('Enter Fasting Blood Sugar: ')
    restecg = st.selectbox('Select type of Rest ECG abnormalities:', ['normal', 'ST-T wave abnormality', 'left ventricular hypertrophy'])
    exang = st.selectbox('Is it exercise induced angina:', ['yes', 'no'])
    slope = st.selectbox('Select type of slope of ST/heart rate:', ['upsloping', 'flat', 'downsloping'])
    ca = st.number_input('Enter number of colored cells: (0, 1, 2, 3): ')
    thal = st.selectbox('Enter Thalassemia classification:', ['error', 'fixed defect', 'normal', 'reversible defect'])

    # Convert gender input to numeric value
    sex_numeric = 1 if sex.lower() == 'male' else 0

    return trestbps, oldpeak, sex_numeric, cp, fbs, restecg, exang, slope, ca, thal

# Predict function
def predict_heart_disease(trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal):
    input_data = pd.DataFrame({'trestbps': [trestbps], 'oldpeak': [oldpeak], 'sex': [sex], 'cp': [cp], 'fbs': [fbs],
                               'restecg': [restecg], 'exang': [exang], 'slope': [slope], 'ca': [ca], 'thal': [thal]})

    prediction = best_model.predict(input_data)

    return prediction

# Main function to run the Streamlit app
def main():
    st.title('Heart Disease Prediction')

    # Get user input
    trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal = predict_values()

    # Predict heart disease
    prediction = predict_heart_disease(trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal)

    # Display prediction
    if prediction[0] == 1:
        st.write("YES, YOU HAVE HEART DISEASE")
    else:
        st.write("NO, YOU DONT HAVE HEART DISEASE")

if __name__ == "__main__":
    main()
