from flask import Flask, request, jsonify
import joblib
import re
import numpy as np
import easyocr
from io import BytesIO
from PIL import Image
from flask_cors import CORS

model = joblib.load("health_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en']) 

def preprocess_input_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    return text

def extract_text_from_image(image):
    img = Image.open(BytesIO(image))
    result = reader.readtext(np.array(img), detail=0)
    return " ".join(result)

@app.route('/predict', methods=['POST'])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"].read()

    extracted_text = extract_text_from_image(image)
    ingredients_text = preprocess_input_text(extracted_text)

    features = vectorizer.transform([ingredients_text])
    prediction = model.predict(features)[0]

    status = {2: "Healthy", 1: "Moderately Healthy", 0: "Unhealthy"}
    
    return jsonify({
        "extracted_ingredients": extracted_text.upper(),
        "classification": status[prediction]
    })

if __name__ == '__main__':
    app.run(debug=True)
