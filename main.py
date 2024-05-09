import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_model = joblib.load('heart.pkl')

# Function to predict values
def predict_values():
    print('You will be needing to enter the following 10 values for best results: ')
    trestbps = st.number_input('Enter resting Blood Pressure: ')
    oldpeak = st.number_input('Enter ST depression induced by exercise relative to rest (decimal): ')
    sex = st.selectbox('Select gender:', ['male', 'female'])
    cp = st.selectbox('Select type of Chest Pain:', ['atypical angina', 'typical angina', 'non-anginal', 'asymptomatic'])
    fbs = st.number_input('Enter Fasting Blood Sugar: ')
    restecg = st.selectbox('Select type of Rest ECG abnormalities:', ['normal', 'ST-T wave abnormality', 'left ventricular hypertrophy'])
    exang = st.selectbox('Is it exercise induced angina:', ['yes', 'no'])
    slope = st.selectbox('Select type of slope of ST/heart rate:', ['upsloping', 'flat', 'downsloping'])
    ca = st.number_input('Enter number of colored cells: (0, 1, 2, 3): ', min_value=0, max_value=3, step=1)
    thal = st.selectbox('Enter Thalassemia classification:', ['error', 'fixed defect', 'normal', 'reversible defect'])

    return trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal

# Predict function
def predict_heart_disease(trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal):
    input_data = pd.DataFrame({'trestbps': [trestbps], 'oldpeak': [oldpeak], 'sex_1': [1 if sex == 'male' else 0],
                               'cp_1': [1 if cp == 'atypical angina' else 0], 'cp_2': [1 if cp == 'typical angina' else 0],
                               'cp_3': [1 if cp == 'non-anginal' else 0], 'fbs_1': [1 if fbs > 120 else 0], 'restecg_1': [1 if restecg == 'normal' else 0],
                               'restecg_2': [1 if restecg == 'ST-T wave abnormality' else 0], 'exang_1': [1 if exang == 'yes' else 0],
                               'slope_1': [1 if slope == 'upsloping' else 0], 'ca_1': [1 if ca == 0 else 0], 'ca_2': [1 if ca == 1 else 0],
                               'ca_3': [1 if ca == 2 else 0], 'ca_4': [1 if ca == 3 else 0], 'thal_1': [1 if thal == 'error' else 0],
                               'thal_3': [1 if thal == 'reversible defect' else 0]})

    prediction = best_model.predict(input_data)

    return prediction

# Main function to run the Streamlit app
def main():
    st.title('Heart Disease Prediction')

    # Get user input
    trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal = predict_values()

    # Submit button
    if st.button('Predict'):
        # Predict heart disease
        prediction = predict_heart_disease(trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal)

        # Display prediction
        if prediction[0] == 1:
            st.write("YES, YOU HAVE HEART DISEASE")
        else:
            st.write("NO, YOU DONT HAVE HEART DISEASE")

if __name__ == "__main__":
    main()
