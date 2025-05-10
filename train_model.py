import pandas as pd
import numpy as np
import nltk
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv("ingredients_health_status.csv")

df["Ingredients"] = df["Ingredients"].str.lower()

df = df.groupby("Ingredients")["Healthy status"].max().reset_index()

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = " ".join(word for word in text.split() if word not in stop_words)
    return text.lower()

df["Ingredients"] = df["Ingredients"].apply(preprocess_text)

X = df["Ingredients"]
y = df["Healthy status"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model, "health_classifier.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
