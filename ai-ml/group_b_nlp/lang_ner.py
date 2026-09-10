import re
import spacy
from langdetect import detect

# Load the small English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

from shared.contracts import EvidenceCandidate

def analyze_text(text: str) -> dict:
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
        lang = detect(text)
    except:
        lang = "unknown"
        
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "LOC"]:
            entities.append(ent.text)
            
    # Simple regex for BTC addresses (Base58, starting with 1, 3, or bc1)
    btc_pattern = r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{39,59})\b'
    crypto_addresses = re.findall(btc_pattern, text)
    
    return {
        "language": lang,
        "entities": list(set(entities)),
        "crypto_addresses": list(set(crypto_addresses))
    }
