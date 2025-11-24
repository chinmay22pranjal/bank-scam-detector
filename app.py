from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load model
model = joblib.load('models/fraud_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [float(x) for x in request.form.values()]
        prediction = model.predict([data])[0]
        result = "Fraudulent Transaction" if prediction == 1 else "Legitimate Transaction"
        return render_template('index.html', prediction_text=f"Prediction: {result}")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
