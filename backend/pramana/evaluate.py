"""
EVALUATION HARNESS.  The ONLY file permitted to read answer_key.csv.

Produces the ablation that is the entire demo:
    naive additive scoring  vs  independence-aware capped fusion
"""

import csv
import os
import sys
from pathlib import Path

try:
    from pramana.stub_features_a import emit_all
    from pramana.rarity import RarityIndex, TAU, REFERENCE_POPULATION
    from pramana import score_naive, score_pramana
except ModuleNotFoundError:
    from stub_features_a import emit_all
    from rarity import RarityIndex, TAU, REFERENCE_POPULATION
    import score_naive, score_pramana


def _resolve_file(filename):
    if os.path.exists(filename):
        return filename
    pkg_file = Path(__file__).parent / filename
    if pkg_file.exists():
        return str(pkg_file)
    return filename


def load_key(path=None):
    key_path = _resolve_file(path or "answer_key.csv")
    return dict(r for r in list(csv.reader(open(key_path, "r", encoding="utf-8")))[1:])


def confusion(preds, truth):
    tp = sum(1 for p, t in zip(preds, truth) if p and t)
    fp = sum(1 for p, t in zip(preds, truth) if p and not t)
    fn = sum(1 for p, t in zip(preds, truth) if not p and t)
    tn = sum(1 for p, t in zip(preds, truth) if not p and not t)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    fmr = fp / (fp + tn) if fp + tn else 0.0        # false-merge rate
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=prec, recall=rec,
                f1=f1, false_merge_rate=fmr)


def run(lam=score_pramana.LAMBDA, tau=None, quiet=False, grouping=True):
    accounts, pairs, obs_by_pair = emit_all()
    rarity = RarityIndex()
    key = load_key()

    truth, naive_pred, pram_pred, decoys = [], [], [], []
    pram_assessments = {}

    for r in pairs:
        a, b = r["account_a"], r["account_b"]
        pid = f"{a}__{b}"
        obs = obs_by_pair[pid]
        t = key[a] == key[b]

        n = score_naive.score_pair(obs, rarity)
        p = score_pramana.assess(pid, a, b, obs, rarity, accounts, lam=lam,
                                 grouping=grouping)
        pram_assessments[pid] = p

        truth.append(t)
        naive_pred.append(n["merged"])
        pram_pred.append(score_pramana.merged(p))
        if r["note"] == "PLANTED_DECOY":
            decoys.append((pid, n["merged"], score_pramana.merged(p)))

    cn = confusion(naive_pred, truth)
    cp = confusion(pram_pred, truth)
    refused = sum(1 for p in pram_assessments.values()
                  if not p.issued and not p.excluded)

    if not quiet:
        print("=" * 72)
        print("PRAMANA | INDEPENDENCE-ACCOUNTING ABLATION")
        print(f"reference population: {REFERENCE_POPULATION}")
        print(f"asserted params: lambda={lam}  tau={TAU}  k_min="
              f"{score_pramana.K_MIN}  ceiling={score_pramana.CEILING}")
        print("=" * 72)
        print(f"{'':28}{'NAIVE':>12}{'PRAMANA':>12}")
        print("-" * 72)
        rows = [("false merges (count)", cn["fp"], cp["fp"]),
                ("FALSE-MERGE RATE", f"{cn['false_merge_rate']:.1%}",
                 f"{cp['false_merge_rate']:.1%}"),
                ("precision", f"{cn['precision']:.1%}", f"{cp['precision']:.1%}"),
                ("recall", f"{cn['recall']:.1%}", f"{cp['recall']:.1%}"),
                ("F1", f"{cn['f1']:.3f}", f"{cp['f1']:.3f}"),
                ("true merges", cn["tp"], cp["tp"]),
                ("missed links", cn["fn"], cp["fn"])]
        for label, x, y in rows:
            print(f"{label:28}{str(x):>12}{str(y):>12}")
        d_naive = sum(1 for _, n, _ in decoys if n)
        d_pram = sum(1 for _, _, p in decoys if p)
        print("-" * 72)
        print(f"{'PLANTED DECOYS caught':28}{f'{len(decoys)-d_naive}/{len(decoys)}':>12}"
              f"{f'{len(decoys)-d_pram}/{len(decoys)}':>12}")
        print(f"{'assessments REFUSED (k<2)':28}{'n/a':>12}{refused:>12}")
        print("=" * 72)

    return cn, cp, pram_assessments


def balance_sheet(pid, assessments, obs_by_pair=None):
    """Print the Evidence Balance Sheet for one pair. This is the demo."""
    a = assessments[pid]
    print("\n" + "=" * 72)
    print(f"EVIDENCE BALANCE SHEET   {a.account_a}  vs  {a.account_b}")
    print("=" * 72)
    for f in a.families:
        state = f"{f['capped_log_lr']:+.2f}" if f["capped_log_lr"] else " 0.00"
        print(f"  {f['family']}  raw {f['raw_log_lr']:>5.2f}   "
              f"damped {f['damped_log_lr']:>5.2f}   -> {state}")
        for note in f["discount_reason"].split("; "):
            print(f"        - {note}")
    if a.counter_evidence:
        print("\n  COUNTER-EVIDENCE")
        for c in a.counter_evidence:
            print(f"        - [{c['severity']}] {c['contradiction_class']} "
                  f"(-{c['delta']:.2f})")
            print(f"          {c['explanation']}")
    print("\n  k (independent origins)  : "
          f"{a.family_count_k}   over {a.distinct_independence_keys} capture origin(s)")
    if a.excluded:
        print(f"  VERDICT                  : EXCLUDED - {a.refusal_reason}")
    elif not a.issued:
        print(f"  VERDICT                  : NO ASSESSMENT ISSUED")
        print(f"                             {a.refusal_reason}")
    else:
        print(f"  log10 LR                 : {a.log_lr}   [{a.verbal_band}]")
    print(f"  defence hypothesis       : {a.defence_hypothesis}")
    print("=" * 72)


def ablation_table():
    """The headline result: does independence accounting change the behaviour?"""
    import csv as _csv
    cn, cp, A = run(quiet=True)
    _, cg, _ = run(quiet=True, grouping=False)
    pairs_file = _resolve_file("pairs.csv")
    notes = {f"{r['account_a']}__{r['account_b']}": r["note"]
             for r in _csv.DictReader(open(pairs_file, "r", encoding="utf-8"))}
    key = load_key()
    fp = [notes[p] or "ordinary_negative" for p, a in A.items()
          if score_pramana.merged(a) and key[a.account_a] != key[a.account_b]]
    from collections import Counter
    refused = sum(1 for a in A.values() if not a.issued and not a.excluded)

    try:
        import pramana.rarity as R
    except ModuleNotFoundError:
        import rarity as R
    print("=" * 78)
    print("PRAMANA | INDEPENDENCE-ACCOUNTING ABLATION      RANGE-SIM v0.1")
    print(f"asserted priors: lambda={score_pramana.LAMBDA}  tau={R.TAU}  "
          f"k_min={score_pramana.K_MIN}  ceiling={score_pramana.CEILING}  "
          f"(design priors, NOT fitted)")
    print("=" * 78)
    print(f"{'':30}{'NAIVE':>14}{'no grouping':>16}{'PRAMANA':>14}")
    print("-" * 78)
    rows = [("FALSE-MERGE RATE", f"{cn['false_merge_rate']:.1%}",
             f"{cg['false_merge_rate']:.1%}", f"{cp['false_merge_rate']:.1%}"),
            ("false merges (count)", cn["fp"], cg["fp"], cp["fp"]),
            ("precision", f"{cn['precision']:.1%}", f"{cg['precision']:.1%}",
             f"{cp['precision']:.1%}"),
            ("recall", f"{cn['recall']:.1%}", f"{cg['recall']:.1%}",
             f"{cp['recall']:.1%}"),
            ("F1", f"{cn['f1']:.3f}", f"{cg['f1']:.3f}", f"{cp['f1']:.3f}")]
    for label, x, y, z in rows:
        print(f"{label:30}{str(x):>14}{str(y):>16}{str(z):>14}")
    print("-" * 78)
    print(f"{'assessments REFUSED (k<2)':30}{'n/a':>14}{'':>16}{refused:>14}")
    print("=" * 78)
    print("RESIDUAL FAILURES (the 12 remaining false merges):")
    for cls, n in Counter(fp).most_common():
        print(f"    {n:>3}  {cls}")
    print()
    print("  The handover cases are the residual risk named in the threat model:")
    print("  a resold account genuinely inherits the seller's identifiers, so")
    print("  correlation has no basis on which to separate the two operators.")
    print("=" * 78)
    return A


if __name__ == "__main__":
    ablation_table()
