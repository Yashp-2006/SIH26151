"""
Parse PGP public key blocks using pgpy.
"""
import pgpy


def parse_pgp_key(block: str) -> dict:
    """
    Parse an ASCII-armored PGP public key block.
    Returns dict with: algorithm, key_size, created, subkeys, uids.
    Returns {"error": reason} on parse failure.
    """
    try:
        key, _ = pgpy.PGPKey.from_blob(block)
    except Exception as exc:
        return {"error": str(exc)}

    pk = key._key  # primary key packet

    # Algorithm name
    algo = pk.pkalg.name if hasattr(pk, "pkalg") else "unknown"

    # Key size (RSA: key_size attr; EC: curve name)
    try:
        key_size = pk.keymaterial.key_size
    except AttributeError:
        try:
            key_size = pk.keymaterial.curve.name
        except AttributeError:
            key_size = None

    # Creation timestamp
    created = str(key.created) if key.created else None

    # Subkeys
    subkeys = []
    for sk_id, sk in key._children.items():
        sk_algo = sk._key.pkalg.name if hasattr(sk._key, "pkalg") else "unknown"
        subkeys.append({"key_id": str(sk_id), "algorithm": sk_algo})

    # UIDs
    uids = [str(uid) for uid in key.userids]

    return {
        "algorithm": algo,
        "key_size": key_size,
        "created": created,
        "subkeys": subkeys,
        "uids": uids,
    }
