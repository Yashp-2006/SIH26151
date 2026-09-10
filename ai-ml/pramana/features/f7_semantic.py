import sys
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

_AIML_DIR = Path(__file__).resolve().parent.parent.parent
if str(_AIML_DIR) not in sys.path:
    sys.path.insert(0, str(_AIML_DIR))

from shared.contracts import EvidenceCandidate

DETECTOR_VERSION = "f7_semantic_lda_v0.1"

class SemanticTopicModeler:
    """
    Evidence Family F7: Semantic/Topic Modeling.
    Uses Latent Dirichlet Allocation (LDA) to extract underlying themes 
    and output a probabilistic match score between two text corpus distributions.
    """
    def __init__(self, n_components=5):
        self.vectorizer = CountVectorizer(stop_words='english', max_features=1000)
        self.lda = LatentDirichletAllocation(n_components=n_components, random_state=42)
        self.is_fitted = False

    def fit(self, texts: list[str]):
        if not texts:
            return
        X = self.vectorizer.fit_transform(texts)
        self.lda.fit(X)
        self.is_fitted = True

    def _get_topic_distribution(self, text: str):
        if not self.is_fitted or not text.strip():
            return None
        X = self.vectorizer.transform([text])
        return self.lda.transform(X)[0]

    def compute_similarity(self, text_a: str, text_b: str) -> float:
        dist_a = self._get_topic_distribution(text_a)
        dist_b = self._get_topic_distribution(text_b)
        
        if dist_a is None or dist_b is None:
            return 0.0
            
        # Compute Jensen-Shannon Divergence or simple dot product
        dot = sum(a * b for a, b in zip(dist_a, dist_b))
        return round(float(dot), 4)

def build_f7_candidate(subject_a: str, subject_b: str, text_a: str, text_b: str, modeler: SemanticTopicModeler, doc_ref: str) -> EvidenceCandidate:
    sim = modeler.compute_similarity(text_a, text_b)
    
    # Cap for F7 Semantic is 1.0 (from README)
    raw_score = round(sim * 1.0, 3)
    
    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F7",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=f"semantic::{subject_a}__{subject_b}",
        polarity="+" if sim >= 0.5 else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={"topic_similarity": sim}
    )
