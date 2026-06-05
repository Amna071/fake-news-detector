# 📰 TruthLens — Fake News Detector
### Multi-Category AI-Powered Fake News Detection System

---

## 📁 Project Structure

```
fake_news_detector/
│
├── model/
│   └── fake_news_training.ipynb    ← Google Colab training notebook
│
├── backend/
│   ├── app.py                      ← Flask REST API
│   ├── requirements.txt            ← Python dependencies
│   └── fake_news_model.pkl         ← (place here after training)
│
└── frontend/
    └── index.html                  ← Web UI (open in browser or VS Code)
```

---

## 🗂️ DATASETS — Which to Use

### Your Current Dataset (ISOT)
- ✅ Politics & Economics only
- Source: Kaggle → `clmentbisaillon/fake-and-real-news-dataset`

### Additional Datasets for More Categories

| Dataset | Categories | Size | Kaggle Link |
|---------|-----------|------|-------------|
| **WELFake** | Sports, Entertainment, Tech, Health, General | ~72,000 | `saurabhshahane/fake-news-classification` |
| **LIAR** | Politics, Health, History, Finance | ~12,800 | `mrisdal/fake-news` |
| **FakeNewsNet** | Health, Entertainment | ~20,000 | Search on Kaggle |

> 💡 **Recommended**: Use ISOT + WELFake together. The notebook already handles this combination and adds synthetic samples for all categories (Health, Tech, Entertainment, History, Sports).

---

## 🚀 SETUP GUIDE — Step by Step

---

### PART 1: Train Model in Google Colab

**Step 1:** Go to [colab.research.google.com](https://colab.research.google.com)

**Step 2:** Click `File → Upload Notebook` and select `model/fake_news_training.ipynb`

**Step 3:** Get your Kaggle API key:
- Go to [kaggle.com/settings](https://www.kaggle.com/settings)
- Scroll to **API** section
- Click **Create New Token**
- It downloads `kaggle.json`

**Step 4:** Run all cells one by one (Shift+Enter):
- Cell 1: Installs libraries
- Cell 2: Upload kaggle.json when prompted
- Cell 3-4: Downloads ISOT + WELFake datasets
- Cell 5-9: Trains the model
- Cell 10: Saves model
- Cell 11: **Downloads** `fake_news_model.pkl` to your computer

**Step 5:** Copy `fake_news_model.pkl` into the `backend/` folder.

> ✅ Expected accuracy: **88–95%** with both datasets

---

### PART 2: Run Backend (Flask API)

**Requirements:** Python 3.8 or higher

**Step 1:** Open a terminal/command prompt

**Step 2:** Navigate to the backend folder:
```bash
cd fake_news_detector/backend
```

**Step 3:** Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Step 4:** Start the Flask server:
```bash
python app.py
```

**Step 5:** You should see:
```
✅ Model loaded successfully!
🚀 Starting Fake News Detector API...
📍 Running at: http://localhost:5000
```

> ⚠️ Keep this terminal window open while using the app!

---

### PART 3: Open Frontend in VS Code

**Step 1:** Open VS Code

**Step 2:** Open the `fake_news_detector` folder:
- `File → Open Folder → select fake_news_detector`

**Step 3:** Install the **Live Server** extension:
- Click Extensions icon (Ctrl+Shift+X)
- Search: `Live Server` by Ritwick Dey
- Click Install

**Step 4:** Open `frontend/index.html`

**Step 5:** Right-click the file → **Open with Live Server**

**Step 6:** Browser opens at `http://127.0.0.1:5500/frontend/index.html`

---

## 🧪 How to Use

1. **Select a Category** (Health, Tech, Entertainment, etc.)
2. **Paste a news headline or article** into the text box
3. Click **ANALYZE NEWS**
4. See the result: FAKE or REAL with confidence score

### Test Examples

**Should be FAKE:**
> Doctors reveal drinking bleach cures COVID-19 according to secret government documents

**Should be REAL:**
> CDC recommends annual flu vaccines for all individuals six months and older

---

## 📊 Model Details

| Property | Value |
|----------|-------|
| Algorithm | Logistic Regression |
| Features | TF-IDF (50,000 features, unigrams + bigrams) |
| Training data | ISOT + WELFake + Synthetic samples |
| Target accuracy | 80%+ (typically 88–95%) |

---

## ❓ Troubleshooting

**"API Offline" shown in frontend**
→ Make sure you ran `python app.py` in the backend folder and it says "Running at localhost:5000"

**Model not loading**
→ Make sure `fake_news_model.pkl` is inside the `backend/` folder (not anywhere else)

**pip install errors on Windows**
→ Try: `python -m pip install -r requirements.txt`

**CORS errors in browser console**
→ Use Live Server extension in VS Code, not just opening the HTML file directly

**Low accuracy in Colab**
→ Make sure both datasets downloaded correctly. Check cell 6 output for "Total dataset size"
