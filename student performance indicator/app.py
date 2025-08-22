from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
model = joblib.load('best_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=["POST"])
def predict():
    data = request.form.to_dict()
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return render_template('index.html', prediction_text=f'Predicted test Score: {prediction:.2f}')

if __name__ == "__main__":
    app.run(debug=True)