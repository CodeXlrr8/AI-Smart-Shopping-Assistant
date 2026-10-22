# Project Methodology — Final Prototype

## Problem
Online shopping requires users to compare products across sources, inspect specifications, read many reviews, evaluate price differences, and manually track price changes.

## Proposed solution
The system uses a multi-agent architecture to decompose shopping research into specialized tasks. LangGraph coordinates the agents while FastAPI exposes the workflow to the React frontend.

## Methodology

### Phase 1 — Requirement analysis
Extract:
- product category
- budget
- use cases
- brand preferences
- mandatory features
- preferred features

### Phase 2 — Product research
Retrieve product name, model, source, price, availability, rating, review count, specifications, and review text from an authorized API. A small laptop catalogue is retained as a deterministic demo fallback.

### Phase 3 — Specification normalization
Map different field names and units into a common structure so products can be compared consistently.

### Phase 4 — Review analysis
Summarize available review evidence and identify recurring positive/negative signals.

### Phase 5 — Suspicious-review detection
Use TF-IDF n-gram features with Logistic Regression as the baseline supervised classifier. For research evaluation, the project provides a downloader/evaluator for the Ott et al. Deceptive Opinion Spam Corpus.

The Ott corpus contains 1,600 labeled hotel reviews split between truthful and deceptive reviews. It is used only to evaluate the deception-classification component; it is not claimed to be a product-review dataset.

### Phase 6 — Price comparison and tracking
Select the lowest observed price, store price snapshots, and compare observations against configured alert thresholds.

### Phase 7 — Value-for-money ranking
The prototype combines user fit, specification quality, review evidence, price, and review reliability into a weighted score.

### Phase 8 — Recommendation
Return the highest-scoring candidate together with evidence-based explanation. An optional LLM can rewrite the explanation without inventing product facts.

### Phase 9 — Evaluation
Evaluate the suspicious-review classifier with a held-out test split using accuracy, precision, recall, F1-score, and confusion matrix. Evaluate the end-to-end shopping workflow with functional test cases covering budget, RAM, use case, price, and unavailable API scenarios.

## Limitations
- The deception classifier is trained on hotel reviews, so domain transfer to product reviews is a research limitation.
- Real-time product and price coverage depends on the authorized API configured by the user.
- The prototype's weighted ranking is a transparent heuristic rather than a learned ranking model.
