# Review Dataset

## Research evaluation dataset
The final evaluation pipeline uses:

**Ott et al. (2011), Deceptive Opinion Spam Corpus v1.4**

- 1,600 hotel reviews
- truthful and deceptive labels
- 20 Chicago hotels
- balanced corpus

Official paper and dataset page:
https://aclanthology.org/P11-1032/

Dataset attachment:
https://aclanthology.org/attachments/P11-1032.Datasets.zip

The repository does not redistribute the corpus. Run:

```bash
python download_review_dataset.py
python evaluate_fake_review_model.py
```

The evaluator writes metrics to `review_model_metrics.json`.

## Important limitation
This is a hotel-review deception corpus, not an e-commerce product-review corpus. Therefore, evaluation demonstrates the suspicious-review classification pipeline but does not prove that the model generalizes to product reviews.
