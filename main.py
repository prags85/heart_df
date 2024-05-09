import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_model = joblib.load('heart_prediction.pkl')

# Function to predict values
def predict_values():
    st.write('Please enter the following information for accurate prediction:')
    trestbps = st.number_input('Resting Blood Pressure (mm Hg):', min_value=0)
    oldpeak = st.number_input('ST Depression induced by exercise relative to rest (mm):', min_value=0.0)
    sex = st.radio('Gender:', ['Male', 'Female'])
    cp = st.selectbox('Chest Pain Type:', ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])
    fbs = st.radio('Fasting Blood Sugar (> 120 mg/dl):', ['Yes', 'No'])
    restecg = st.selectbox('Resting Electrocardiographic Results:', ['Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy'])
    exang = st.radio('Exercise Induced Angina:', ['Yes', 'No'])
    slope = st.selectbox('Slope of the peak exercise ST segment:', ['Upsloping', 'Flat', 'Downsloping'])
    ca = st.selectbox('Number of Major Vessels Colored by Fluoroscopy:', ['0', '1', '2', '3'])
    thal = st.selectbox('Thalassemia:', ['Normal', 'Fixed Defect', 'Reversible Defect'])

    return trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal

# Predict function
def predict_heart_disease(trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal):
    sex_numeric = 1 if sex == 'Male' else 0
    fbs_numeric = 1 if fbs == 'Yes' else 0

    # One-hot encoding for categorical variables
    cp_encoded = [0] * 4
    cp_encoded[['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'].index(cp)] = 1

    restecg_encoded = [0] * 3
    restecg_encoded[['Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy'].index(restecg)] = 1

    exang_numeric = 1 if exang == 'Yes' else 0

    slope_encoded = [0] * 3
    slope_encoded[['Upsloping', 'Flat', 'Downsloping'].index(slope)] = 1

    ca_encoded = [0] * 4
    ca_encoded[int(ca)] = 1

    thal_encoded = [0] * 3
    thal_encoded[['Normal', 'Fixed Defect', 'Reversible Defect'].index(thal)] = 1

    input_data = pd.DataFrame({'trestbps': [trestbps], 'oldpeak': [oldpeak], 'sex': [sex_numeric],
                               'cp_0': [cp_encoded[0]], 'cp_1': [cp_encoded[1]], 'cp_2': [cp_encoded[2]], 'cp_3': [cp_encoded[3]],
                               'fbs': [fbs_numeric], 'restecg_0': [restecg_encoded[0]], 'restecg_1': [restecg_encoded[1]], 'restecg_2': [restecg_encoded[2]],
                               'exang': [exang_numeric], 'slope_0': [slope_encoded[0]], 'slope_1': [slope_encoded[1]], 'slope_2': [slope_encoded[2]],
                               'ca_0': [ca_encoded[0]], 'ca_1': [ca_encoded[1]], 'ca_2': [ca_encoded[2]], 'ca_3': [ca_encoded[3]],
                               'thal_0': [thal_encoded[0]], 'thal_1': [thal_encoded[1]], 'thal_2': [thal_encoded[2]]})

    prediction = best_model.predict(input_data)

    return prediction[0]

# Main function to run the Streamlit app
def main():
    st.title('Heart Disease Prediction')

    # Get user input
    trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal = predict_values()

    # Predict heart disease
    prediction = predict_heart_disease(trestbps, oldpeak, sex, cp, fbs, restecg, exang, slope, ca, thal)

    # Display prediction
    if prediction == 1:
        st.error("Warning: You have a high risk of heart disease.")
    else:
        st.success("Congratulations: You seem to be at a low risk of heart disease.")

if __name__ == "__main__":
    main()
