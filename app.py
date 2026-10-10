from flask import Flask, render_template, request, jsonify
from langdetect import detect
from deep_translator import GoogleTranslator
import pyttsx3

app = Flask(__name__)

# Load knowledge base
import json
with open("intents.json") as f:
    intents = json.load(f)

# Voice engine
engine = pyttsx3.init()

# Step 1: Intent detection (simple rule-based)
def get_intent(text):
    text = text.lower()
    for intent, keywords in intents.items():
        for word in keywords:
            if word in text:
                return intent
    return "unknown"

# Step 2: Generate response
def get_response(intent):
    responses = {
        "greeting": "Hello! How can I help you?",
        "fees": "The course fee is 50,000 INR",
        "courses": "We offer MCA, BCA, and AI courses",
        "unknown": "Sorry, I didn't understand"
    }
    return responses[intent]

# Route: UI
@app.route("/")
def home():
    return render_template("index.html")

# Route: Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    # Step 3: Detect language
    lang = detect(user_input)

    # Step 4: Translate to English
    translated = GoogleTranslator(source='auto', target='en').translate(user_input)

    # Step 5: NLP (intent detection)
    intent = get_intent(translated)

    # Step 6: Get response
    response = get_response(intent)

    # Step 7: Translate back to user language
    final_response = GoogleTranslator(source='en', target=lang).translate(response)

    # Step 8: Voice output (optional)
    engine.say(final_response)
    engine.runAndWait()

    return jsonify({"reply": final_response})

if __name__ == "__main__":
    app.run(debug=True)