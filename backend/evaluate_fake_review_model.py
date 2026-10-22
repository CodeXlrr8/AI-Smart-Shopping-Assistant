"""Evaluate the suspicious-review classifier on the Ott Deceptive Opinion Spam Corpus.

Run after download_review_dataset.py. The evaluator discovers .txt files and
infers labels from directory/file names containing truthful/deceptive or
truthful/deceptive class markers.
"""
from pathlib import Path
import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

BASE = Path(__file__).resolve().parent
DATA_ROOT = BASE / "data" / "op_spam_v1.4"
OUT = BASE / "data" / "review_model_metrics.json"


def infer_label(path: Path):
    parts = [p.lower() for p in path.parts]
    name = path.name.lower()
    joined = "/".join(parts) + "/" + name
    if any(token in joined for token in ["deceptive", "/d_", "\\d_"]):
        return 1
    if any(token in joined for token in ["truthful", "/t_", "\\t_"]):
        return 0
    if re.search(r"(?:^|[_\\/])d(?:[_\\.]|$)", name):
        return 1
    if re.search(r"(?:^|[_\\/])t(?:[_\\.]|$)", name):
        return 0
    return None


def load_corpus():
    rows = []
    for path in DATA_ROOT.rglob("*.txt"):
        label = infer_label(path)
        if label is None:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            rows.append((text, label))
    if not rows:
        raise FileNotFoundError(
            f"No labeled .txt reviews found under {DATA_ROOT}. "
            "Run: python download_review_dataset.py"
        )
    return rows


def main():
    rows = load_corpus()
    texts = [x[0] for x in rows]
    labels = [x[1] for x in rows]
    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=42, stratify=labels
    )
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ])
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    cm = confusion_matrix(y_test, pred).tolist()
    metrics = {
        "dataset": "Ott et al. Deceptive Opinion Spam Corpus v1.4",
        "total_reviews": len(rows),
        "test_reviews": len(y_test),
        "test_size": 0.20,
        "random_state": 42,
        "model": "TF-IDF (1-2 grams) + Logistic Regression",
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision_deceptive": round(float(precision_score(y_test, pred, zero_division=0)), 4),
        "recall_deceptive": round(float(recall_score(y_test, pred, zero_division=0)), 4),
        "f1_deceptive": round(float(f1_score(y_test, pred, zero_division=0)), 4),
        "confusion_matrix": cm,
        "classification_report": classification_report(y_test, pred, target_names=["truthful", "deceptive"], zero_division=0),
    }
    OUT.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"Saved metrics to {OUT}")


if __name__ == "__main__":
    main()
