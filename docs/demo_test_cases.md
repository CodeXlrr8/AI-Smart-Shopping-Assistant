# Demo Test Cases

## Test 1 — AI/ML laptop
Input:
`Laptop for AI/ML and coding under ₹70000 with 16GB RAM`

Expected:
- budget extracted as 70000
- AI/ML and coding detected
- 16GB RAM treated as mandatory
- products ranked by transparent weighted score

## Test 2 — Gaming laptop
Input:
`Gaming laptop under ₹80000 with 16GB RAM`

Expected:
- gaming detected
- products with RTX-class GPU receive a fit adjustment
- price and specification scores change with the budget

## Test 3 — College portability
Input:
`Laptop for college under ₹60000`

Expected:
- college use case detected
- lighter products receive a portability adjustment when weight is available

## Test 4 — Price alert
1. Search for a product.
2. Click **Set price alert**.
3. Enter a target below the current price.
4. Call `POST /api/price-check` during the demo.
5. Verify the alert remains active until a current price is at or below the target.

## Test 5 — ML review detector
After downloading the Ott corpus and restarting the backend:

```bash
cd backend
python download_review_dataset.py
python evaluate_fake_review_model.py
```

Verify that `review_model_metrics.json` contains accuracy, precision, recall, F1, and confusion matrix.

## Test 6 — API fallback
Run without `PRODUCT_API_URL`.

Expected:
- research mode reports demo fallback
- the laptop catalogue still produces recommendations

## Test 7 — External API
Configure `PRODUCT_API_URL` and `PRODUCT_API_KEY` for an authorized provider whose response contains `products`, `items`, or `results`.

Expected:
- research mode reports external API
- returned products are normalized before ranking
