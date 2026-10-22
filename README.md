# AI Smart Shopping Assistant — Final Prototype

A multi-agent shopping research assistant built with **React, FastAPI, LangGraph, Python, SQLAlchemy, and optional LLM integration**.

## Core workflow

Requirement Analysis → Product Research → Specification Normalization → Review Analysis → Suspicious Review Detection → Price Comparison → Value-for-Money Ranking → Recommendation

## Main features

- Natural-language shopping requirements
- Multi-agent orchestration with LangGraph
- Authorized product API integration with deterministic demo fallback
- Specification normalization
- Review analysis
- TF-IDF + Logistic Regression suspicious-review classifier
- Price comparison and persistent price history
- Target-price alerts
- Scheduled price checks
- Optional LLM-generated explanation
- Accessory recommendations
- React frontend
- SQLite by default / PostgreSQL-ready configuration

## Data

The demo product catalogue is a small structured laptop catalogue used for deterministic end-to-end demonstrations.

For research evaluation of suspicious-review detection, the project uses the **Ott et al. Deceptive Opinion Spam Corpus v1.4**. It contains 1,600 labeled hotel reviews split between truthful and deceptive classes. The project includes a downloader and evaluator rather than redistributing the corpus.

See `backend/data/DATASET.md`.

## Setup

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### ML evaluation

```bash
cd backend
python download_review_dataset.py
python evaluate_fake_review_model.py
```

Metrics are written to `backend/data/review_model_metrics.json`.

## Configuration

- `OPENAI_API_KEY`: optional LLM explanation
- `PRODUCT_API_URL`: authorized product API endpoint
- `PRODUCT_API_KEY`: API credential
- `DATABASE_URL`: SQLite or PostgreSQL connection string
- `PRICE_CHECK_INTERVAL_MINUTES`: background price-check interval; `0` disables it

## Academic evaluation notes

The suspicious-review model is a research baseline, not a production fraud detector. Its benchmark domain is hotel reviews, so product-review domain transfer is a limitation. Report accuracy, precision, recall, F1-score, and confusion matrix instead of claiming universal fake-review detection.

## Project documentation

- `docs/system_architecture.md` — architecture and data flow
- `docs/project_methodology.md` — methodology and limitations
- `docs/presentation_script.md` — 7-minute presentation script
- `docs/viva_questions.md` — likely viva/judge questions


## Deployment

### Backend — Render

This repository includes `render.yaml`. Create a Render Web Service from the repository, or configure the service with root directory `backend`, build command `pip install -r requirements.txt`, and start command `uvicorn main:app --host 0.0.0.0 --port $PORT`. Set `DATABASE_URL` to a hosted PostgreSQL connection string for persistent production data, and set `FRONTEND_URLS` to the deployed frontend URL.

### Frontend — Vercel

Deploy the `frontend` directory as a Vite/React project. Set `VITE_API_URL` to the deployed Render backend URL, for example `https://YOUR-BACKEND.onrender.com`.

### Local development

Copy `frontend/.env.example` to `frontend/.env.local` and set `VITE_API_URL=http://localhost:8000`.
# AI-Smart-Shopping-Assistant
