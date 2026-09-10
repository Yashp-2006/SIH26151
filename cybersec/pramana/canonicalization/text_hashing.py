"""Text hashing and shingling for deterministic canonicalization."""

import hashlib
import json
import re
from typing import Optional, Set

# Simple ASCII/alphanumeric tokenizer for deterministic hashing
_WORD_RE = re.compile(r'\w+')

def _tokenize(text: str) -> list[str]:
    # We do NOT perform aggressive normalization (like lowercasing or stemming) 
    # to preserve original prose differences, unless specified. But SimHash
    # typically uses lowercase to be robust against case changes.
    # The frozen spec says: "Do NOT rewrite prose" and "preserve Unicode".
    # We will lowercase for the hashing token stream but retain raw text.
    return _WORD_RE.findall(text.lower())

def compute_sha256(title: Optional[str], description: Optional[str]) -> str:
    """text-pair-json-v2: SHA-256 of a framed UTF-8 JSON pair.

    None and empty remain distinct; embedded separators cannot alias fields.
    This digest is a comparison operand, never a canonical origin identity.
    """
    h = hashlib.sha256()
    payload = json.dumps([title, description], ensure_ascii=False,
                         separators=(",", ":")).encode('utf-8')
    h.update(payload)
    return h.hexdigest()

def compute_shingles(title: Optional[str], description: Optional[str], n: int = 3) -> Set[str]:
    """Compute n-gram word shingles."""
    t = title if title is not None else ""
    d = description if description is not None else ""
    tokens = _tokenize(t + " " + d)
    shingles = set()
    if len(tokens) < n:
        if tokens:
            shingles.add(" ".join(tokens))
        return shingles
        
    for i in range(len(tokens) - n + 1):
        shingles.add(" ".join(tokens[i:i+n]))
    return shingles

def _hash_token(token: str) -> int:
    """64-bit hash of a token using SHA-256 for deterministic distribution."""
    h = hashlib.sha256(token.encode('utf-8')).digest()
    # Take first 8 bytes as a 64-bit integer
    return int.from_bytes(h[:8], byteorder='big')

def compute_simhash(title: Optional[str], description: Optional[str]) -> int:
    """Compute a 64-bit SimHash over word bigrams."""
    t = title if title is not None else ""
    d = description if description is not None else ""
    tokens = _tokenize(t + " " + d)
    
    if not tokens:
        return 0
        
    # Use bigrams as features
    features = []
    for i in range(len(tokens) - 1):
        features.append(tokens[i] + " " + tokens[i+1])
    if not features and tokens:
        features = tokens

    v = [0] * 64
    for feature in features:
        h = _hash_token(feature)
        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                v[i] += 1
            else:
                v[i] -= 1
                
    fingerprint = 0
    for i in range(64):
        if v[i] > 0:
            fingerprint |= (1 << i)
            
    return fingerprint

def hamming_distance(hash1: int, hash2: int) -> int:
    """Compute bitwise Hamming distance between two 64-bit integers."""
    x = hash1 ^ hash2
    return bin(x).count('1')

def compute_containment(shingles1: Set[str], shingles2: Set[str]) -> tuple[float, float, float]:
    """
    Returns (jaccard, containment_1_in_2, containment_2_in_1).
    Containment X in Y = len(intersection) / len(X).
    """
    if not shingles1 and not shingles2:
        return 1.0, 1.0, 1.0
    if not shingles1:
        return 0.0, 1.0, 0.0
    if not shingles2:
        return 0.0, 0.0, 1.0
        
    intersection = len(shingles1 & shingles2)
    union = len(shingles1 | shingles2)
    
    jaccard = intersection / union
    c1_in_2 = intersection / len(shingles1)
    c2_in_1 = intersection / len(shingles2)
    
    return jaccard, c1_in_2, c2_in_1
