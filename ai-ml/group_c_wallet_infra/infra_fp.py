from shared.contracts import EvidenceCandidate

def fingerprint_infra(metadata: dict) -> dict:
    return {
        "tls_subject": metadata.get("tls", {}).get("subject", ""),
        "tls_san": metadata.get("tls", {}).get("san", []),
        "favicon_hash": metadata.get("favicon_hash", ""),
        "headers": metadata.get("headers", {})
    }
