from flask import Flask, request, jsonify
import numpy as np
import joblib
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load model (you only have the trained model, no need for training data)
model = joblib.load('model/best_logistic_model.joblib')

@app.route('/model-info', methods=['GET'])
def get_model_info():
    try:
        # Basic model information
        coefficients = model.coef_[0]  # Coefficients for each feature
        intercept = model.intercept_[0]  # Intercept of the model
        features = ['Pclass', 'Sex', 'Age', 'Fare', 'Embarked']
        
        # Create a dictionary with feature names and their corresponding coefficients
        coef_dict = {feature: float(coef) for feature, coef in zip(features, coefficients)}
        coef_dict['Intercept'] = float(intercept)

        # Model parameters (for Logistic Regression)
        model_params = {
            'solver': model.get_params()['solver'],
            'max_iter': model.get_params()['max_iter'],
            'penalty': model.get_params()['penalty'],
            'C': float(model.get_params()['C'])
        }

        model_info = {
            'model_name': 'Logistic Regression',
            'coefficients': coef_dict,
            'n_features': len(features),
            'features': features,
            'classes': model.classes_.tolist(),
            'model_parameters': model_params
        }

        return jsonify(model_info)

    except Exception as e:
        print(f"Error in fetching model info: {str(e)}")  # Logging error for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Titanic Survival Prediction API is running."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Ambil data dari request JSON
    sex = 1 if data['sex'] == 'male' else 0
    age = float(data['age'])
    fare = float(data['fare'])
    pclass = int(data['pclass'])
    embark = 1 if data['embarked'] == 'C' else (2 if data['embarked'] == 'Q' else 3)

    # Bentuk array input untuk model
    input_data = np.array([[sex, age, fare, pclass, embark]])

    # Prediksi hasil (0 atau 1)
    prediction = model.predict(input_data)[0]

    # Hitung probabilitas prediksi
    probability = model.predict_proba(input_data)[0][1]  # Probabilitas untuk kelas 'Survived'

    # Tentukan hasil prediksi
    result = "Survived" if prediction == 1 else "Not Survived"

    # Kembalikan hasil dalam format JSON
    return jsonify({'result': result, 'probability': probability})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
