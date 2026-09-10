import re
import spacy
from langdetect import DetectorFactory
from langdetect.detector_factory import PROFILES_DIRECTORY

def load_ner_model():
    """Model installation is an explicit setup step, never an import side effect."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError as exc:
        raise RuntimeError("NER model unavailable; install en_core_web_sm explicitly") from exc


from shared.contracts import EvidenceCandidate

def analyze_text(text: str, *, nlp=None) -> dict:
    """
    Language detection and NER. Extract names, orgs, locations, and crypto addresses.
    """
    if not text.strip():
        return {
            "language": "unknown",
            "entities": [],
            "crypto_addresses": []
        }
        
    try:
        factory = DetectorFactory()
        factory.seed = 0
        factory.load_profile(PROFILES_DIRECTORY)
        detector = factory.create()
        detector.append(text)
        lang = detector.detect()
    except Exception:
        lang = "unknown"
        
    doc = (nlp if nlp is not None else load_ner_model())(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "LOC"]:
            entities.append(ent.text)
            
    # Simple regex for BTC addresses (Base58, starting with 1, 3, or bc1)
    btc_pattern = r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{39,59})\b'
    crypto_addresses = re.findall(btc_pattern, text)
    
    return {
        "language": lang,
        "entities": sorted(set(entities)),
        "crypto_addresses": sorted(set(crypto_addresses))
    }
