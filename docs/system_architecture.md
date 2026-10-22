# System Architecture — AI Smart Shopping Assistant

## 1. High-level architecture

```text
User
  |
  v
React Frontend
  |
  v
FastAPI REST API
  |
  v
LangGraph Orchestrator
  |
  +--> Requirement Analysis Agent
  |
  +--> Product Research Agent ----> Authorized Product API
  |                                  |
  |                                  +--> Demo catalogue fallback
  |
  +--> Specification Analysis Agent
  |
  +--> Review Analysis Agent ------> TF-IDF + Logistic Regression
  |                                  |
  |                                  +--> suspicious-review probability
  |
  +--> Price Comparison Agent -----> Price snapshots / history
  |
  +--> Value-for-Money Ranking Agent
  |
  +--> Recommendation Agent -------> Optional LLM explanation
  |
  +--> Accessory Recommendation
  |
  v
PostgreSQL / SQLite
  |
  +--> search logs
  +--> price snapshots
  +--> price alerts
```

## 2. Agent responsibilities

| Agent | Responsibility | Output |
|---|---|---|
| Requirement Analysis | Parse budget, use case, mandatory features | User profile |
| Product Research | Retrieve candidate products | Product records |
| Specification Analysis | Standardize fields | Comparable specifications |
| Review Analysis | Extract review evidence | Pros, cons, review summary |
| Suspicious Review Detection | Estimate deceptive/suspicious probability | Review reliability |
| Price Comparison | Compare available prices | Best price/store |
| Value-for-Money | Combine fit, specs, reviews, price, reliability | Ranked products |
| Recommendation | Produce explainable result | Final recommendation |

## 3. Data flow

1. User enters natural-language shopping requirements.
2. Requirement Agent converts the request into structured constraints.
3. Product Research Agent retrieves candidates from an authorized source or demo catalogue.
4. Specification Agent normalizes heterogeneous product fields.
5. Review Agent analyzes available reviews and passes text through the suspicious-review classifier.
6. Price Agent selects the lowest available price and records price observations.
7. Ranking Agent calculates a weighted value score.
8. Recommendation Agent explains the result using available evidence.
9. The API returns products, scores, review signals, price information, and recommendation details to React.

## 4. Storage

SQLite is the default development database. PostgreSQL can be configured with `DATABASE_URL`. The schema stores products, price snapshots, alerts, and search events.

## 5. Background price monitoring

The scheduler periodically invokes the product research flow, records new prices, and checks target-price alerts. The interval is controlled through `PRICE_CHECK_INTERVAL_MINUTES`.
