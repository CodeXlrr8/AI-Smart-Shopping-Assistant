from __future__ import annotations
from pathlib import Path
from typing import Iterable
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE = Path(__file__).resolve().parent
SYNTHETIC_FILE = BASE / 'data' / 'review_training.csv'
REAL_ROOT = BASE / 'data' / 'op_spam_v1.4'


def _infer_label(path: Path):
    joined = '/'.join(p.lower() for p in path.parts) + '/' + path.name.lower()
    if 'deceptive' in joined or re.search(r'(?:^|[/_])d(?:[_\.]|$)', path.name.lower()):
        return 1
    if 'truthful' in joined or re.search(r'(?:^|[/_])t(?:[_\.]|$)', path.name.lower()):
        return 0
    return None


def load_training_data():
    """Prefer the documented Ott corpus when downloaded; otherwise use demo data."""
    if REAL_ROOT.exists():
        texts, labels = [], []
        for path in REAL_ROOT.rglob('*.txt'):
            label = _infer_label(path)
            if label is None:
                continue
            text = path.read_text(encoding='utf-8', errors='ignore').strip()
            if text:
                texts.append(text)
                labels.append(label)
        if len(texts) >= 100 and len(set(labels)) == 2:
            return texts, labels, 'Ott et al. Deceptive Opinion Spam Corpus v1.4'

    import csv
    texts, labels = [], []
    with SYNTHETIC_FILE.open('r', encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            texts.append(row['review'])
            labels.append(int(row['label']))
    return texts, labels, 'synthetic demo review set'


def build_model() -> tuple[Pipeline, str]:
    texts, labels, source = load_training_data()
    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
        ('clf', LogisticRegression(max_iter=2000, class_weight='balanced')),
    ])
    model.fit(texts, labels)
    return model, source


MODEL, MODEL_SOURCE = build_model()


def predict_reviews(reviews: Iterable[str]):
    reviews = [str(r) for r in reviews]
    if not reviews:
        return []
    probs = MODEL.predict_proba(reviews)[:, 1]
    return [
        {
            'text': text,
            'suspicious_probability': round(float(prob), 3),
            'suspicious': bool(prob >= 0.60),
            'model_source': MODEL_SOURCE,
        }
        for text, prob in zip(reviews, probs)
    ]
