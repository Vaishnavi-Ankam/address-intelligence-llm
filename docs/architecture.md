# Architecture Notes

## Main workflow

1. Read employee and KB tables from BigQuery.
2. Convert KB rows into retrievable documents.
3. Rewrite retrieval queries using an instruction-tuned LLM.
4. Retrieve candidate docs with embeddings + FAISS.
5. Rerank retrieved docs with a cross-encoder.
6. Standardize the address using retrieved context.
7. Estimate commute distance / time and calculate confidence.
8. Decide eligibility.
9. Trigger manual review when confidence or formatting is weak.
10. Evaluate base model vs fine-tuned model and write results back to BigQuery.

## Agents used

- Retrieval Agent
- Address Standardization Agent
- Commute & Confidence Agent
- Eligibility Agent
- Escalation Agent
- Coordinator Agent


NOTE: the notebooks run independently for training and testing purpose
