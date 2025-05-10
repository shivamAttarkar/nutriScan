import base64
import json
from flask import Flask, request, jsonify
import joblib
import re
import numpy as np
import easyocr
import os
import httpx
from io import BytesIO
from PIL import Image
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
model = joblib.load("health_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

POCKETBASE_URL = os.getenv("POCKETBASE_URL")
OLLAMA_URL = os.getenv("OLLAMA_URL")

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

def classify_ingredients(ingredients_list):
    statuses = {2: "Healthy", 1: "Moderately Healthy", 0: "Unhealthy"}
    preprocessed = [preprocess_input_text(ing) for ing in ingredients_list if ing.strip() != ""]
    if not preprocessed:
        return []
    features = vectorizer.transform(preprocessed)
    predictions = model.predict(features)
    result = []
    healthy = unhealthy = moderately_healthy = 0
    for ingredient, prediction in zip(ingredients_list, predictions):
        result.append({
            "ingredient": ingredient.upper(),
            "status": statuses[prediction]
        })
        healthy += 1 if prediction == 2 else 0
        moderately_healthy += 1 if prediction == 1 else 0
        unhealthy += 1 if prediction == 0 else 0
    return result, {"Healthy":healthy, "Moderately Healthy": moderately_healthy, "Unhealthy":unhealthy}

def cleanText(text):
    json_body = {
        "model":"llama3.2:1b-instruct-q4_K_S",
        "prompt":f'classify the ingredients and give ingredient names seperated by commas {text}'
    }
    res = request(f'{OLLAMA_URL}/api/generate', json=jsonify(json_body))
    return res

def createRecord(image, classification, extracted_text, classified_ingredients, count):
    data = {
        "_method": "POST",
        "count": json.dumps(count),
        "classified_ingredients": json.dumps(classified_ingredients),
        "extracted_text": extracted_text.upper(),
        "classification": classification
    }
    files = {
        "image": (image.filename, image.stream, image.mimetype)
    }

    with httpx.Client() as client:
        response = client.post(
            f"{POCKETBASE_URL}/api/collections/predictions/records",
            data=data,
            files=files
        )

    if response.status_code == 200:
        return True
    else:
        print("Error:", response.status_code, response.text)
        return False


@app.route('/predict', methods=['POST'])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    imagefile = request.files["image"]
    image = imagefile.read()

    extracted_text = extract_text_from_image(image)
    print(cleanText(extracted_text))
    ingredients_text = preprocess_input_text(extracted_text)

    ingredients_list = re.split(r',|\n', extracted_text)
    classified_ingredients, count = classify_ingredients(ingredients_list)

    features = vectorizer.transform([ingredients_text])
    prediction = model.predict(features)[0]

    status = {2: "Healthy", 1: "Moderately Healthy", 0: "Unhealthy"}

    # createRecord(image=imagefile, classification=status[prediction], extracted_text=extracted_text, 
    # classified_ingredients=classified_ingredients, count=count)
    
    return jsonify({
        "classification": status[prediction],
        "extracted_ingredients": extracted_text.upper(),
        "classified_ingredients": classified_ingredients,
        "count":count
    })

if __name__ == '__main__':
    app.run(debug=True)
