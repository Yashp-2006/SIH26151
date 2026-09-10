"""Validated synthetic inputs. Defaults never depend on the working directory.

This is not the CyberSec evidence-promotion contract (DC-06 remains deferred).
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent


def data_path(path, default):
    return Path(path) if path is not None else DATA_DIR / default


def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def load_accounts(path=None):
    with data_path(path, "accounts.json").open(encoding="utf-8") as stream:
        rows = json.load(stream)
    if not isinstance(rows, list) or not rows:
        raise ValueError("Reference population must be a nonempty account list")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Account must be an object")
        for field in ("account_id", "pgp_fp", "asn", "contact_id", "template_id", "infra_batch"):
            nonempty(row.get(field), field)
        if row["account_id"] in seen:
            raise ValueError("Duplicate account_id in reference population")
        seen.add(row["account_id"])
        if not isinstance(row.get("listings"), list):
            raise ValueError("listings must be a list")
        for listing in row["listings"]:
            if not isinstance(listing, dict):
                raise ValueError("Listing must be an object")
            for field in ("image_id", "capture_batch"):
                nonempty(listing.get(field), field)
    return rows
