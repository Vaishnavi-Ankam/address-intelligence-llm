import json
from typing import Dict, Any, List

from .utils import safe_json_loads
from .prompts import SYSTEM_PROMPT_ADDRESS_AGENT
from .retrieval import retrieval_agent


def run_chat_prompt(system_prompt: str, user_prompt: str, text_generation_pipeline, tokenizer) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    output = text_generation_pipeline(prompt)[0]["generated_text"]
    return output[len(prompt):].strip()


def build_user_prompt_for_address_agent(raw_home_address: str, office_address: str, retrieved_context: List[dict]) -> str:
    return json.dumps(
        {
            "raw_home_address": raw_home_address,
            "office_address": office_address,
            "retrieved_context": retrieved_context,
        },
        indent=2,
    )


def address_standardization_agent(raw_home_address, office_address, retrieved_context, text_generation_pipeline, tokenizer):
    output = run_chat_prompt(
        SYSTEM_PROMPT_ADDRESS_AGENT,
        build_user_prompt_for_address_agent(raw_home_address, office_address, retrieved_context),
        text_generation_pipeline,
        tokenizer,
    )
    try:
        return safe_json_loads(output)
    except Exception:
        return {
            "corrected_standardized_address": raw_home_address,
            "correction_confidence": 0.5,
            "standardization_reason": "Fallback parsing used because model output was not valid JSON.",
        }


def heuristic_commute_estimate(home_address: str, office_address: str):
    text = home_address.lower()
    if "cupertino" in text or "california" in text:
        return 2100.0, 2100
    if "new york" in text:
        return 900.0, 900
    if "atlanta" in text:
        return 250.0, 250
    if "springfield" in text or "illinois" in text:
        return 430.0, 430
    if "franklin" in text or "brentwood" in text:
        return 20.0, 30
    if "nashville" in text:
        return 8.0, 20
    return 35.0, 45


def commute_and_confidence_agent(corrected_standardized_address, office_address, correction_confidence, retrieved_context):
    distance_miles, commute_minutes = heuristic_commute_estimate(corrected_standardized_address, office_address)
    rerank_scores = [x.get("rerank_score", 0.0) or 0.0 for x in retrieved_context]
    avg_rerank = sum(rerank_scores) / len(rerank_scores) if rerank_scores else 0.0
    geocode_match_quality = "high" if correction_confidence >= 0.85 else "medium" if correction_confidence >= 0.65 else "low"
    combined_confidence = min(0.99, max(0.05, 0.65 * float(correction_confidence) + 0.35 * min(max(avg_rerank, 0.0), 1.0)))
    manual_review_trigger_signals = []
    if correction_confidence < 0.75:
        manual_review_trigger_signals.append("low_address_correction_confidence")
    if geocode_match_quality == "low":
        manual_review_trigger_signals.append("low_geocode_match_quality")
    if distance_miles is None:
        manual_review_trigger_signals.append("missing_commute_distance")
    return {
        "travel_distance_miles": float(distance_miles) if distance_miles is not None else None,
        "estimated_commute_minutes": int(commute_minutes) if commute_minutes is not None else None,
        "geocode_match_quality": geocode_match_quality,
        "combined_confidence_score": round(float(combined_confidence), 4),
        "manual_review_trigger_signals": manual_review_trigger_signals,
    }


def eligibility_agent(travel_distance_miles, combined_confidence_score):
    if travel_distance_miles is None:
        return {"eligibility_decision": "manual_review", "eligibility_reason": "Distance could not be computed."}
    if travel_distance_miles <= 60 and combined_confidence_score >= 0.55:
        return {"eligibility_decision": "Eligible", "eligibility_reason": "Distance is within 60 miles and confidence is above threshold."}
    if travel_distance_miles > 60:
        return {"eligibility_decision": "Not eligible", "eligibility_reason": "Distance is greater than 60 miles."}
    return {"eligibility_decision": "manual_review", "eligibility_reason": "Distance is within threshold but confidence is not high enough."}


def escalation_agent(correction_confidence, manual_review_trigger_signals, eligibility_decision, corrected_standardized_address):
    reasons = list(manual_review_trigger_signals)
    if eligibility_decision == "manual_review":
        reasons.append("eligibility_rule_requires_review")
    if "," not in corrected_standardized_address:
        reasons.append("address_format_still_looks_incomplete")
    return {
        "manual_review_required": len(reasons) > 0,
        "escalation_reason": "; ".join(reasons) if reasons else "no_escalation_needed",
    }


def coordinator_agent(employee_row, vectorstore, text_generation_pipeline, tokenizer, reranker_model):
    raw_home_address = employee_row["raw_home_address"]
    office_address = employee_row["office_address"]
    retrieval_output = retrieval_agent(
        raw_home_address=raw_home_address,
        office_address=office_address,
        vectorstore=vectorstore,
        text_generation_pipeline=text_generation_pipeline,
        tokenizer=tokenizer,
        reranker_model=reranker_model,
        candidate_k=8,
        top_k=4,
    )
    address_output = address_standardization_agent(
        raw_home_address=raw_home_address,
        office_address=office_address,
        retrieved_context=retrieval_output["retrieved_context"],
        text_generation_pipeline=text_generation_pipeline,
        tokenizer=tokenizer,
    )
    commute_output = commute_and_confidence_agent(
        corrected_standardized_address=address_output["corrected_standardized_address"],
        office_address=office_address,
        correction_confidence=address_output["correction_confidence"],
        retrieved_context=retrieval_output["retrieved_context"],
    )
    eligibility_output = eligibility_agent(
        travel_distance_miles=commute_output["travel_distance_miles"],
        combined_confidence_score=commute_output["combined_confidence_score"],
    )
    escalation_output = escalation_agent(
        correction_confidence=address_output["correction_confidence"],
        manual_review_trigger_signals=commute_output["manual_review_trigger_signals"],
        eligibility_decision=eligibility_output["eligibility_decision"],
        corrected_standardized_address=address_output["corrected_standardized_address"],
    )
    return {
        "employee_id": employee_row.get("employee_id"),
        "employee_name": employee_row.get("employee_name"),
        "raw_home_address": raw_home_address,
        "office_address": office_address,
        "corrected_standardized_address": address_output["corrected_standardized_address"],
        "correction_confidence": address_output["correction_confidence"],
        "travel_distance_miles": commute_output["travel_distance_miles"],
        "estimated_commute_minutes": commute_output["estimated_commute_minutes"],
        "eligibility_decision": eligibility_output["eligibility_decision"],
        "manual_review_required": escalation_output["manual_review_required"],
        "escalation_reason": escalation_output["escalation_reason"],
        "retrieved_context": retrieval_output["retrieved_context"],
    }
