from shared.contracts import EvidenceCandidate
from group_b_nlp.stylometry import extract_style_features

def _compute_distance(feat1: dict, feat2: dict) -> float:
    # simple jaccard or count difference over function words
    words1 = feat1.get("function_words", {})
    words2 = feat2.get("function_words", {})
    all_keys = set(words1.keys()).union(words2.keys())
    if not all_keys:
        return 0.0
    diff = sum(abs(words1.get(k, 0) - words2.get(k, 0)) for k in all_keys)
    return diff / len(all_keys)

def detect_style_shift(documents: list[str]) -> list[dict]:
    if not documents:
        return []
        
    features = [extract_style_features(doc) for doc in documents]
    
    shifts = []
    # Compare each document to the previous one
    for i in range(len(features)):
        if i == 0:
            shifts.append({"doc_index": i, "shift_score": 0.0})
        else:
            score = _compute_distance(features[i-1], features[i])
            shifts.append({"doc_index": i, "shift_score": score})
            
    return shifts
