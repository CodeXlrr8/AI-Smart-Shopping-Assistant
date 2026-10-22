# 7-Minute Presentation Script

## Slide 1 — Title (30 sec)
Good morning respected judges. We are presenting our **AI Smart Shopping Assistant using Generative AI and Agentic AI**. The goal is to reduce the time and effort required to research products online.

## Slide 2 — Problem (45 sec)
Online shopping is not simply about finding a product. Users have to compare products across sources, understand specifications, read many reviews, identify suspicious review signals, compare prices, and monitor price changes. This becomes difficult when the user has a specific budget and multiple requirements.

## Slide 3 — Proposed Solution (45 sec)
Our solution is a multi-agent shopping assistant. Instead of asking one model to perform every task, we divide the workflow into specialized agents for requirements, product research, specifications, reviews, price comparison, ranking, and recommendation.

## Slide 4 — Architecture (60 sec)
The frontend is built with React and communicates with a FastAPI backend. LangGraph orchestrates the agent workflow. Product research uses an authorized product API with a demo fallback. Review analysis includes a TF-IDF plus Logistic Regression suspicious-review classifier. SQLite is used by default, with PostgreSQL configuration supported. An optional LLM generates the final explanation.

## Slide 5 — Agent Workflow (60 sec)
First, the Requirement Agent converts natural language into structured constraints. Product Research retrieves candidates. Specification Analysis standardizes them. Review Analysis extracts evidence and suspicious-review signals. Price Comparison finds the best available price. The Value-for-Money Agent combines the evidence into a transparent score. Finally, the Recommendation Agent explains the result.

## Slide 6 — ML Component (60 sec)
For suspicious-review detection, we use TF-IDF features with Logistic Regression. For research evaluation we use the Ott Deceptive Opinion Spam Corpus, which contains 1,600 labeled hotel reviews. We evaluate using a held-out test set and report accuracy, precision, recall, F1-score, and the confusion matrix. We clearly treat this as a deception-detection benchmark and not as a product-review dataset.

## Slide 7 — Price Tracking and Alerts (45 sec)
The system stores price snapshots and supports target-price alerts. A background scheduler can periodically check the configured product source. This converts the assistant from a one-time comparison tool into a system that can continue tracking a user's purchase decision.

## Slide 8 — Output / Demo (45 sec)
The user receives ranked products, normalized specifications, price information, review signals, a match score, an explanation, and optional accessory recommendations. During the demo, we can change the budget or use case and show how the ranking changes.

## Slide 9 — Research Gap and Conclusion (45 sec)
Existing approaches often address recommendation, review analysis, fake-review detection, or price comparison as separate tasks. Our prototype combines these components into one agentic workflow. The result is an explainable shopping research pipeline rather than a simple product recommender.

## Closing
Thank you. We are ready for questions.
