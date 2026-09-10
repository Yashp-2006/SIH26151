"""
Extract BTC addresses, PGP block markers, onion v3 addresses,
email/Jabber/Telegram identifiers from raw text.
"""
import re

_BTC_LEGACY   = re.compile(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b')
_BTC_BECH32   = re.compile(r'\bbc1[a-z0-9]{25,90}\b')
_PGP_START    = re.compile(r'-----BEGIN PGP PUBLIC KEY BLOCK-----')
_PGP_END      = re.compile(r'-----END PGP PUBLIC KEY BLOCK-----')
_ONION_V3     = re.compile(r'\b[a-z2-7]{56}\.onion\b')
_EMAIL        = re.compile(r'\b[\w.+-]+@[\w.-]+\.\w{2,}\b')
_JABBER       = re.compile(r'\b[\w.+-]+@(?:jabber|xmpp)\.[\w.-]+\.\w{2,}\b')
_TELEGRAM     = re.compile(r'(?:t\.me|telegram\.me)/[\w]{5,}')


def extract_indicators(text: str) -> list:
    """Return list of dicts with keys: type, value."""
    results = []

    for m in _BTC_LEGACY.finditer(text):
        results.append({"type": "btc_legacy", "value": m.group()})
    for m in _BTC_BECH32.finditer(text):
        results.append({"type": "btc_bech32", "value": m.group()})

    # PGP block markers (start/end pairs)
    for m in _PGP_START.finditer(text):
        results.append({"type": "pgp_block_start", "value": m.group()})
    for m in _PGP_END.finditer(text):
        results.append({"type": "pgp_block_end", "value": m.group()})

    for m in _ONION_V3.finditer(text):
        results.append({"type": "onion_v3", "value": m.group()})

    # Jabber before generic email (more specific)
    jabber_hits = set()
    for m in _JABBER.finditer(text):
        results.append({"type": "jabber", "value": m.group()})
        jabber_hits.add(m.group())
    for m in _EMAIL.finditer(text):
        if m.group() not in jabber_hits:
            results.append({"type": "email", "value": m.group()})

    for m in _TELEGRAM.finditer(text):
        results.append({"type": "telegram", "value": m.group()})

    return results
