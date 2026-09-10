"""
Test suite for Group A deterministic modules.
Pulls test data from HF dataset repo; checks against synthetic_ground_truth.json.
"""
import os
import sys
import json
import tempfile

from dotenv import load_dotenv
from huggingface_hub import hf_hub_download

load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_REPO  = os.environ.get("HF_DATASET_REPO", "yashai2006/pramana-synthetic-list-a")

# Ensure parent is on path so shared/ resolves
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from group_a_deterministic.extractors   import extract_indicators
from group_a_deterministic.canonicalise import canonicalise_text, are_near_duplicates, canonicalise_image, images_are_near_duplicates
from group_a_deterministic.pgp_meta     import parse_pgp_key
from group_a_deterministic.rarity       import compute_rarity


def _hf(filename: str) -> str:
    """Download a file from the HF dataset repo and return local path."""
    return hf_hub_download(
        repo_id=HF_REPO, filename=filename, repo_type="dataset", token=HF_TOKEN
    )


def _load_ground_truth() -> dict:
    path = _hf("synthetic_ground_truth.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── helpers ──────────────────────────────────────────────────────────────────

def check(label: str, passed: bool) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {label}")
    return passed


# ── individual test functions ─────────────────────────────────────────────────

def test_extractors(gt: dict) -> int:
    print("\n=== extractors.py ===")
    failures = 0

    # Grab the first vendor listing and confirm basic extraction types work
    first_file = next(iter(next(iter(gt["template_families"].values()))))
    text = open(_hf(first_file), encoding="utf-8", errors="ignore").read()
    results = extract_indicators(text)
    types_found = {r["type"] for r in results}

    if not check("returns list", isinstance(results, list)):
        failures += 1
    if not check("pgp_block_start detected", "pgp_block_start" in types_found):
        failures += 1

    return failures


def test_canonicalise_text(gt: dict) -> int:
    print("\n=== canonicalise.py (text) ===")
    failures = 0

    pairs = gt.get("near_duplicate_pairs", [])
    if not pairs:
        print("  [SKIP] no near_duplicate_pairs in ground truth")
        return 0

    orig_file, dup_file = pairs[0]
    orig_text = open(_hf(orig_file), encoding="utf-8", errors="ignore").read()
    dup_text  = open(_hf(dup_file),  encoding="utf-8", errors="ignore").read()

    if not check("canonicalise_text returns str", isinstance(canonicalise_text(orig_text), str)):
        failures += 1
    if not check("near-dup pair detected", are_near_duplicates(orig_text, dup_text)):
        failures += 1

    return failures


def test_canonicalise_image(gt: dict) -> int:
    print("\n=== canonicalise.py (image) ===")
    failures = 0

    pairs = gt.get("duplicate_image_pairs", [])
    if not pairs:
        print("  [SKIP] no duplicate_image_pairs in ground truth")
        return 0

    orig_file, dup_file = pairs[0]
    with tempfile.TemporaryDirectory() as tmp:
        orig_path = _hf(orig_file)
        dup_path  = _hf(dup_file)

        if not check("canonicalise_image returns str", isinstance(canonicalise_image(orig_path), str)):
            failures += 1
        if not check("image near-dup pair detected", images_are_near_duplicates(orig_path, dup_path)):
            failures += 1

    return failures


def test_pgp_meta(gt: dict) -> int:
    print("\n=== pgp_meta.py ===")
    failures = 0

    # Pull a listing that's known to contain a shared key
    shared = gt.get("shared_pgp_keys", {})
    if not shared:
        print("  [SKIP] no shared_pgp_keys in ground truth")
        return 0

    key_id   = next(iter(shared))
    filename = shared[key_id][0]
    text = open(_hf(filename), encoding="utf-8", errors="ignore").read()

    # Extract PGP block
    start = text.find("-----BEGIN PGP PUBLIC KEY BLOCK-----")
    end   = text.find("-----END PGP PUBLIC KEY BLOCK-----")
    if start == -1 or end == -1:
        print("  [SKIP] no PGP block found in first shared-key file")
        return 0

    block = text[start: end + len("-----END PGP PUBLIC KEY BLOCK-----")]
    result = parse_pgp_key(block)

    if not check("parse_pgp_key returns dict", isinstance(result, dict)):
        failures += 1
        return failures
    if not check("no parse error", "error" not in result):
        failures += 1
    if not check("algorithm present", "algorithm" in result):
        failures += 1
    if not check("uids present", "uids" in result and len(result["uids"]) > 0):
        failures += 1

    return failures


def test_rarity(gt: dict) -> int:
    print("\n=== rarity.py ===")
    failures = 0

    # Build a tiny corpus_counts from wallet_clusters or shared keys to get real data
    corpus_counts = {}
    for cluster in gt.get("wallet_clusters", []):
        for addr in cluster:
            corpus_counts[addr] = corpus_counts.get(addr, 0) + 1

    # Pad a hub indicator (appears > 12 times)
    hub_addr = "1FAKEHUBADDRESS"
    corpus_counts[hub_addr] = 15

    score, is_hub = compute_rarity(hub_addr, corpus_counts)
    if not check("hub detected (count>12)", is_hub):
        failures += 1
    if not check("rarity_score is float", isinstance(score, float)):
        failures += 1

    rare_addr = "1RAREADDRNOTINCORPUS"
    score2, is_hub2 = compute_rarity(rare_addr, corpus_counts)
    if not check("unseen = not hub", not is_hub2):
        failures += 1
    if not check("unseen = inf rarity", score2 == float("inf")):
        failures += 1

    return failures


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    print("Loading ground truth from HF repo …")
    try:
        gt = _load_ground_truth()
    except Exception as exc:
        print(f"FATAL: could not load ground truth — {exc}")
        sys.exit(1)

    total_failures = 0
    total_failures += test_extractors(gt)
    total_failures += test_canonicalise_text(gt)
    total_failures += test_canonicalise_image(gt)
    total_failures += test_pgp_meta(gt)
    total_failures += test_rarity(gt)

    print(f"\n{'='*40}")
    if total_failures == 0:
        print("All tests PASSED.")
    else:
        print(f"{total_failures} test(s) FAILED.")
        sys.exit(1)


if __name__ == "__main__":
    main()
