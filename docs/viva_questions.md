# Viva / Judge Questions and Answers

### 1. Why did you use LangGraph?
LangGraph provides explicit stateful orchestration for a multi-step agent workflow. Each specialized agent updates shared state, making the pipeline easier to control and debug than an unconstrained single-agent loop.

### 2. Why not use one LLM for everything?
Different tasks have different requirements. Product retrieval and price comparison need structured data and deterministic logic, while natural-language understanding and explanation benefit from an LLM. The hybrid architecture separates those responsibilities.

### 3. What dataset is used for fake-review detection?
The evaluation pipeline uses the Ott et al. Deceptive Opinion Spam Corpus. It contains 1,600 labeled hotel reviews, with truthful and deceptive classes. We do not claim it represents product reviews directly.

### 4. Why TF-IDF?
TF-IDF is computationally lightweight, interpretable, and suitable as a strong baseline for text classification. It also makes the prototype easy to evaluate and reproduce.

### 5. Why Logistic Regression?
Logistic Regression works well with sparse TF-IDF text features, provides class probabilities, and is fast enough for a prototype API.

### 6. Can the model detect every fake review?
No. Deceptive-review detection is difficult and domain-dependent. The model produces a probability signal, not a definitive proof that a review is fake.

### 7. How is the final product score calculated?
The prototype combines user fit, specification score, review score, price score, and review reliability using explicit weights. The weights are transparent and can be tuned or learned in future work.

### 8. How do you get real product prices?
The system is API-ready. A product source is configured through `PRODUCT_API_URL` and `PRODUCT_API_KEY`. The project does not rely on scraping sites that prohibit automated collection.

### 9. What happens if the API is unavailable?
The system falls back to the bundled deterministic laptop catalogue so the end-to-end prototype can still be demonstrated.

### 10. Why use both agents and traditional ML?
Agents orchestrate tasks and decisions across services, while the ML classifier performs a focused prediction task. They solve different parts of the system.

### 11. Why use an LLM if ranking is already implemented?
The ranking logic determines the recommendation from structured evidence. The optional LLM is used to turn that evidence into a concise natural-language explanation without inventing product facts.

### 12. What is the major limitation?
The fake-review model is trained on hotel-review data, so domain transfer to product reviews is not guaranteed. Real product API coverage is also dependent on the configured provider.

### 13. How can the project be improved?
Future work can use domain-specific product-review labels, multilingual review models, learned ranking, richer reviewer-level signals, uncertainty calibration, and multiple authorized product/price sources.
