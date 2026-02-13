from flask import Flask, render_template, request, jsonify, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr

app = Flask(__name__)

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ar": "Arabic"
}

# ---------------------------
# Home
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)

# ---------------------------
# TRANSLATE (AUTO-DETECT + PIVOT)
# ---------------------------
@app.route("/translate", methods=["POST"])
def translate():
    text = request.form["text"].strip()
    target = request.form["target"]

    if not text:
        return jsonify({"translated": ""})

    try:
        # Step 1: AUTO detect → English
        text_en = GoogleTranslator(source="auto", target="en").translate(text)

        # Step 2: English → Target
        if target != "en":
            final_text = GoogleTranslator(source="en", target=target).translate(text_en)
        else:
            final_text = text_en

        return jsonify({"translated": final_text})

    except Exception as e:
        return jsonify({"translated": "Translation failed"})

# ---------------------------
# TEXT → VOICE
# ---------------------------
@app.route("/speak", methods=["POST"])
def speak():
    text = request.form["text"]
    lang = request.form["lang"]

    filename = "speech.mp3"
    gTTS(text=text, lang=lang).save(filename)

    return send_file(filename, as_attachment=False)

# ---------------------------
# VOICE → TEXT
# ---------------------------
@app.route("/voice")
def voice():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        # Indian languages auto-detect
        text = r.recognize_google(audio, language="en-IN")
    except:
        text = "Could not recognize speech"

    return jsonify({"text": text})

# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
