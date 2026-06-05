from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# ── Load Model ──────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'fake_news_model.pkl')

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Model not found! Please place fake_news_model.pkl in the backend/ folder.")
    model = None

# ── Preprocessing (must match training) ─────────────────────────────────────
STOP_WORDS = {
    'i','me','my','myself','we','our','ours','ourselves','you','your','yours',
    'he','him','his','she','her','hers','it','its','they','them','their',
    'what','which','who','whom','this','that','these','those','am','is','are',
    'was','were','be','been','being','have','has','had','do','does','did',
    'will','would','could','should','may','might','shall','can','ought','to',
    'of','in','on','at','by','for','with','about','against','between','through',
    'a','an','the','and','but','or','nor','so','yet','both','either','neither',
    'not','no','nor','only','own','same','than','too','very','just','because',
    'as','until','while','during','before','after','above','below','up','down',
    'out','off','over','under','again','then','once','here','there','when',
    'where','why','how','all','any','each','few','more','most','other','some',
    'such','into','if','than','said','also','from','been','its','their','there'
}

def preprocess(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split()
    tokens = [w for w in tokens if w not in STOP_WORDS and len(w) > 2]
    return ' '.join(tokens)

# ── Category keywords for confidence boost ──────────────────────────────────
FAKE_INDICATORS = [
    'secret', 'conspiracy', 'cover-up', 'coverup', 'hoax', 'fraud',
    'exposed', 'shocking', 'breaking', 'exclusive', 'you won\'t believe',
    'mainstream media won\'t', 'they don\'t want', 'hidden truth',
    'wake up', 'sheeple', 'illuminati', 'deep state', 'false flag',
    'crisis actor', 'staged', 'fake', 'clone', 'reptilian', 'lizard'
]

REAL_INDICATORS = [
    'according to', 'research shows', 'study finds', 'experts say',
    'officials confirmed', 'data indicates', 'percent', 'published',
    'university', 'journal', 'government', 'annual report', 'quarterly',
    'announced', 'released', 'survey', 'analysis', 'review'
]

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "message": "Fake News Detector API",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Place fake_news_model.pkl in backend/ folder."}), 503

    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No 'text' field in request body"}), 400

    raw_text = data.get('text', '').strip()
    category = data.get('category', 'General')

    if len(raw_text) < 10:
        return jsonify({"error": "Text is too short. Please provide more content."}), 400

    # Preprocess and predict
    clean = preprocess(raw_text)
    prediction = int(model.predict([clean])[0])
    probabilities = model.predict_proba([clean])[0].tolist()

    confidence = float(max(probabilities)) * 100
    label = "FAKE" if prediction == 1 else "REAL"

    # Textual signal analysis
    lower_text = raw_text.lower()
    fake_signals = [kw for kw in FAKE_INDICATORS if kw in lower_text]
    real_signals = [kw for kw in REAL_INDICATORS if kw in lower_text]

    # Risk level
    if confidence >= 90:
        risk = "Very High" if label == "FAKE" else "Very Reliable"
    elif confidence >= 75:
        risk = "High" if label == "FAKE" else "Reliable"
    elif confidence >= 60:
        risk = "Moderate"
    else:
        risk = "Low / Uncertain"

    return jsonify({
        "result": label,
        "confidence": round(confidence, 2),
        "probabilities": {
            "real": round(probabilities[0] * 100, 2),
            "fake": round(probabilities[1] * 100, 2)
        },
        "risk_level": risk,
        "category": category,
        "fake_signals_found": fake_signals[:5],
        "real_signals_found": real_signals[:5],
        "word_count": len(raw_text.split())
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None})

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🚀 Starting Fake News Detector API...")
    print("📍 Running at: http://localhost:5000")
    print("📌 POST /predict — Send news text to classify")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
