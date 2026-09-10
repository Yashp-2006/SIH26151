"""
Canonicalise text (SHA-256 + SimHash near-dup) and images (pHash).
"""
import hashlib

import imagehash
from PIL import Image


def _simhash(text: str) -> int:
    """64-bit SimHash over word-level shingles."""
    words = text.lower().split()
    v = [0] * 64
    for word in words:
        h = int(hashlib.md5(word.encode()).hexdigest(), 16) & ((1 << 64) - 1)
        for i in range(64):
            v[i] += 1 if (h >> i) & 1 else -1
    bits = 0
    for i in range(64):
        if v[i] > 0:
            bits |= 1 << i
    return bits


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def canonicalise_text(text: str) -> str:
    """
    Returns a stable hash-id for the text.
    Near-duplicates (SimHash Hamming distance <= 3) share the same id as the
    canonical document only when you compare explicitly — this function returns
    the SimHash hex so callers can cluster.
    """
    sh = _simhash(text)
    return format(sh, "016x")


def are_near_duplicates(text_a: str, text_b: str, threshold: int = 3) -> bool:
    """True if two texts are near-duplicates by SimHash."""
    return _hamming(_simhash(text_a), _simhash(text_b)) <= threshold


def sha256_id(text: str) -> str:
    """Exact-match id (SHA-256 hex)."""
    return hashlib.sha256(text.encode()).hexdigest()


def canonicalise_image(path: str) -> str:
    """pHash fingerprint of an image file. Near-dups have Hamming dist <= 10."""
    img = Image.open(path)
    return str(imagehash.phash(img))


def images_are_near_duplicates(path_a: str, path_b: str, threshold: int = 10) -> bool:
    h1 = imagehash.phash(Image.open(path_a))
    h2 = imagehash.phash(Image.open(path_b))
    return (h1 - h2) <= threshold
