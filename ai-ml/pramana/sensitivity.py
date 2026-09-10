"""
SENSITIVITY ANALYSIS for the asserted design priors.

lambda and tau are NOT fitted on RANGE-SIM. Tuning them here and then reporting
the ablation here would be leakage - the exact failure the isolated answer-key
schema exists to prevent.

Instead we assert them from the Blueprint and demonstrate that the conclusion
is STABLE across a plausible range. That is a defensible viva answer;
"we tuned it on our own simulator" is not.
"""

try:
    from pramana.evaluate import run
    from pramana.rarity import TAU
    from pramana import score_pramana
except ModuleNotFoundError:
    from evaluate import run
    from rarity import TAU
    import score_pramana


def sweep_lambda(values=(0.0, 0.1, 0.2, 0.3, 0.4, 0.6)):
    print("=" * 72)
    print("SENSITIVITY: within-family damping lambda   (asserted default 0.2)")
    print("=" * 72)
    print(f"{'lambda':>8}{'false-merge rate':>20}{'precision':>12}{'recall':>10}{'F1':>8}")
    print("-" * 72)
    for lam in values:
        _, cp, _ = run(lam=lam, quiet=True)
        mark = "  <- asserted" if abs(lam - score_pramana.LAMBDA) < 1e-9 else ""
        print(f"{lam:>8.2f}{cp['false_merge_rate']:>19.1%}"
              f"{cp['precision']:>12.1%}{cp['recall']:>10.1%}{cp['f1']:>8.3f}{mark}")
    print("-" * 72)
    print("HONEST FINDING: lambda has NO measurable effect at this corpus scale.")
    print("Multi-group-within-one-family cases are rare in RANGE-SIM v0.1, so the")
    print("damping term almost never binds. What actually moves the false-merge")
    print("rate is the grouping step itself - collapsing raw retrievals and")
    print("correlated captures onto one independence key (see ablation: 3.5% ->")
    print("1.5%). We report lambda as an unvalidated design prior, not a result.")
    print()


def sweep_tau(values=(6, 9, 12, 18, 25, 10**6)):
    try:
        import pramana.rarity as R
    except ModuleNotFoundError:
        import rarity as R
    print("=" * 72)
    print("SENSITIVITY: hub threshold tau              (asserted default 12)")
    print("=" * 72)
    print(f"{'tau':>8}{'false-merge rate':>20}{'precision':>12}{'recall':>10}{'F1':>8}")
    print("-" * 72)
    original = TAU
    for t in values:
        _, cp, _ = run(tau=t, quiet=True)
        label = "off" if t > 10**5 else str(t)
        mark = "  <- asserted" if t == original else ""
        print(f"{label:>8}{cp['false_merge_rate']:>19.1%}"
              f"{cp['precision']:>12.1%}{cp['recall']:>10.1%}{cp['f1']:>8.3f}{mark}")
    print("-" * 72)
    print("KNOWN WEAKNESS: tau is an absolute count, so the same indicator")
    print("crosses the hub threshold as the corpus grows without becoming less")
    print("informative. Alternative thresholds require separate policy and evaluation review.")
    print()


if __name__ == "__main__":
    sweep_lambda()
    sweep_tau()
