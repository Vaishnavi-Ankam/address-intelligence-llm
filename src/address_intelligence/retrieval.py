from typing import List, Dict, Any

from sentence_transformers import CrossEncoder


def build_user_prompt_for_rewriter(raw_home_address: str, office_address: str) -> str:
    return f"""
Raw employee home address:
{raw_home_address}

Assigned office address:
{office_address}

Rewrite this into a retrieval query that will help search the enterprise KB for the best supporting documents.
"""


def rerank_documents(query_text, docs, reranker_model: CrossEncoder, top_k: int = 4):
    pairs = [[query_text, d.page_content] for d in docs]
    scores = reranker_model.predict(pairs)
    scored = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    final_docs = []
    for doc, score in scored[:top_k]:
        doc.metadata["rerank_score"] = float(score)
        final_docs.append(doc)
    return final_docs


def retrieval_agent(
    raw_home_address: str,
    office_address: str,
    vectorstore,
    text_generation_pipeline,
    tokenizer,
    reranker_model,
    candidate_k: int = 8,
    top_k: int = 4,
) -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": "You are a retrieval query rewriting assistant."},
        {"role": "user", "content": build_user_prompt_for_rewriter(raw_home_address, office_address)},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    output = text_generation_pipeline(prompt)[0]["generated_text"]
    rewritten_query = output[len(prompt):].strip()

    candidate_docs = vectorstore.similarity_search(rewritten_query, k=candidate_k)
    final_docs = rerank_documents(rewritten_query, candidate_docs, reranker_model, top_k=top_k)

    return {
        "rewritten_query": rewritten_query,
        "retrieved_context": [
            {
                "doc_id": d.metadata.get("doc_id"),
                "title": d.metadata.get("title"),
                "source_type": d.metadata.get("source_type"),
                "text": d.page_content,
                "rerank_score": d.metadata.get("rerank_score"),
            }
            for d in final_docs
        ],
    }
