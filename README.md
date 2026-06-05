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
    └── index.html                  ← Web UI 


---

## 🗂️ DATASETS

| Dataset | Categories | Size | Kaggle Link |
|---------|-----------|------|-------------|
| **WELFake** | Sports, Entertainment, Tech, Health, General | ~72,000 | `saurabhshahane/fake-news-classification` |
| **LIAR** | Politics, Health, History, Finance | ~12,800 | `mrisdal/fake-news` |
| **FakeNewsNet** | Health, Entertainment | ~20,000 | Search on Kaggle |


