"""
STUB for Person A's evidence generation.
Person B owns this file ONLY until A ships the real extractor. Then delete it.

Reads accounts.json + pairs.csv, emits Observation rows.
Emits NO weights - that is the whole point of the contract.

Independence keys encode capture provenance:
  - asn + template come from ONE site-config scrape  -> share infra_batch
  - images come from a catalogue scrape              -> share capture_batch
  - contact IDs are declared on two separate profiles -> independent per pair
"""

import json
import csv
import os
from pathlib import Path
try:
    from pramana.schema import Observation
except ModuleNotFoundError:
    from schema import Observation



def _resolve_path(filename):
    if os.path.exists(filename):
        return filename
    pkg_file = Path(__file__).parent / filename
    if pkg_file.exists():
        return str(pkg_file)
    return filename


def load(accounts_path=None, pairs_path=None):
    acc_path = _resolve_path(accounts_path or "accounts.json")
    pr_path = _resolve_path(pairs_path or "pairs.csv")
    accounts = {a["account_id"]: a for a in json.load(open(acc_path, "r", encoding="utf-8"))}
    pairs = list(csv.DictReader(open(pr_path, "r", encoding="utf-8")))
    return accounts, pairs


def observations_for_pair(pid, A, B):
    """Everything A can see about this pair. No opinions."""
    obs = []

    # --- F1 cryptographic ------------------------------------------------
    if A["pgp_fp"] == B["pgp_fp"]:
        obs.append(Observation(
            pair_id=pid, family="F1", indicator_type="pgp_fp",
            indicator_value=A["pgp_fp"], match_type="exact",
            independence_key=f"pgpdecl::{pid}"))

    # --- F3 infrastructure -----------------------------------------------
    # asn and template were captured in the same site-config scrape when the
    # infra_batch matches. That is ONE observation opportunity, not two.
    infra_key = (A["infra_batch"] if A["infra_batch"] == B["infra_batch"]
                 else f"infra::{pid}")
    if A["asn"] == B["asn"]:
        obs.append(Observation(
            pair_id=pid, family="F3", indicator_type="asn",
            indicator_value=A["asn"], match_type="exact",
            independence_key=infra_key))

    # --- F5 content artefacts ---------------------------------------------
    if A["template_id"] == B["template_id"]:
        obs.append(Observation(
            pair_id=pid, family="F5", indicator_type="template_id",
            indicator_value=A["template_id"], match_type="simhash",
            independence_key=infra_key))          # same scrape as the ASN

    # mirrored images: many raw retrievals collapse to one canonical artefact
    ia = {l["image_id"]: l["capture_batch"] for l in A["listings"]}
    ib = {l["image_id"]: l["capture_batch"] for l in B["listings"]}
    for img in sorted(set(ia) & set(ib)):
        n_raw = sum(1 for l in A["listings"] + B["listings"]
                    if l["image_id"] == img)
        key = ia[img] if ia[img] == ib[img] else f"img::{pid}::{img}"
        obs.append(Observation(
            pair_id=pid, family="F5", indicator_type="image_id",
            indicator_value=img, match_type="phash",
            independence_key=key, n_raw_hits=n_raw))

    # --- F4 contact --------------------------------------------------------
    if A["contact_id"] == B["contact_id"]:
        obs.append(Observation(
            pair_id=pid, family="F4", indicator_type="contact_id",
            indicator_value=A["contact_id"], match_type="exact",
            independence_key=f"contact::{pid}"))

    return obs


def emit_all(accounts_path=None, pairs_path=None):
    accounts, pairs = load(accounts_path, pairs_path)
    out = {}
    for r in pairs:
        a, b = r["account_a"], r["account_b"]
        pid = f"{a}__{b}"
        out[pid] = observations_for_pair(pid, accounts[a], accounts[b])
    return accounts, pairs, out
