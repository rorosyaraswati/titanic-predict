# Titanic Survival Prediction Web Application

This is a web-based application for predicting Titanic survival using a pre-trained logistic regression model. The project utilizes Flask as the backend framework and Vue.js with Vite and Tailwind CSS for the frontend. 

## Features

- Input passenger details: passenger class, sex, age, passenger fare, and port of embarkation.
- Real-time survival prediction based on user inputs.


## Prerequisites

- Python 3.8 or higher
- Node.js and npm/yarn
- Flask and Vue CLI installed globally

## Setup Instructions

### Backend

1. Navigate to the backend folder:
   ```bash
   cd backend
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the Flask application:
   `python app.py` The backend will be available at http://127.0.0.1:5000

### Frontend

1. Install dependencies:
   `npm install`
2. Start development server:
   `npm run dev` The frontend will be available at http://127.0.0.1:5173

## Model Information
The prediction model (best_logistic_model.joblib) is a logistic regression model trained on the Titanic dataset. It considers features like passenger class, sex, age, fare, and embarked location to make survival predictions.