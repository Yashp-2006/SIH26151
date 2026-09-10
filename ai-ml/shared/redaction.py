import re

# Redaction patterns for deterministic List-A identifiers
_PGP_BLOCK_RE = re.compile(r"-----BEGIN PGP.*?-----END PGP.*?-----", re.DOTALL)
_BTC_RE = re.compile(r"\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{39,59})\b")
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
_URL_RE = re.compile(r"\bhttps?://[^\s]+\b")
_ONION_RE = re.compile(r"\b[a-z2-7]{16,56}\.onion\b")

def redact_identifiers(text: str) -> str:
    """
    Redact deterministic identifiers (PGP blocks, BTC addresses, emails, URLs, onion links)
    to prevent List-A -> List-B leakage. This ensures embeddings and stylometry 
    don't just rediscover List-A artifacts and falsely claim independent evidence.
    """
    if not text:
        return ""
    
    text = _PGP_BLOCK_RE.sub("[PGP_REDACTED]", text)
    text = _BTC_RE.sub("[BTC_REDACTED]", text)
    text = _EMAIL_RE.sub("[EMAIL_REDACTED]", text)
    text = _URL_RE.sub("[URL_REDACTED]", text)
    text = _ONION_RE.sub("[ONION_REDACTED]", text)
    
    return text
