from difflib import SequenceMatcher


def string_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, str(a), str(b)).ratio()


def compare_row(row):
    base_score = row["base_address_similarity"] + row["base_decision_correct"] + row["base_manual_review_correct"]
    ft_score = row["ft_address_similarity"] + row["ft_decision_correct"] + row["ft_manual_review_correct"]
    if ft_score > base_score:
        return "ft_better"
    if ft_score < base_score:
        return "base_better"
    return "tie"
