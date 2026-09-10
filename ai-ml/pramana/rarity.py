"""
Rarity indexing + hub suppression.   OWNED BY PERSON B.

A counts nothing and thresholds nothing. A supplies indicator_value;
B decides what it is worth against a DECLARED reference population.

  weight  = log10(N / count)      IDF-like rarity
  is_hub  = count > TAU           -> contribution forced to ZERO

TAU is an asserted design parameter, not a fitted one. See sensitivity sweep.
"""

import json
import os
from collections import Counter
from pathlib import Path

TAU = 12                    # Blueprint default. Asserted, not tuned.
REFERENCE_POPULATION = "RANGE-SIM v0.1 account corpus"


class RarityIndex:
    def __init__(self, accounts_path=None, *, tau=TAU):
        if type(tau) is not int or tau < 0:
            raise ValueError("tau must be a nonnegative integer")
        self.tau = tau
        try:
            from pramana.data import load_accounts
        except ModuleNotFoundError:
            from data import load_accounts
        accounts = load_accounts(accounts_path)
        self.n = len(accounts)
        self.counts = Counter()
        for a in accounts:
            self.counts[("pgp_fp", a["pgp_fp"])] += 1
            self.counts[("asn", a["asn"])] += 1
            self.counts[("contact_id", a["contact_id"])] += 1
            self.counts[("template_id", a["template_id"])] += 1
            for img in {l["image_id"] for l in a["listings"]}:
                self.counts[("image_id", img)] += 1

    def count(self, itype, value):
        return self.counts.get((itype, value), 1)

    def is_hub(self, itype, value, tau=None):
        return self.count(itype, value) > (self.tau if tau is None else tau)

    def weight(self, itype, value, tau=None):
        """log10 LR contribution of a single indicator, before family rules."""
        tau = self.tau if tau is None else tau
        if type(tau) is not int or tau < 0:
            raise ValueError("tau must be a nonnegative integer")
        c = self.count(itype, value)
        if c > tau:
            return 0.0, f"hub: '{value}' seen {c}x in corpus (tau={tau}) -> forced to 0"
        import math
        w = math.log10(self.n / c)
        return round(w, 3), f"rarity: seen {c}/{self.n} -> log10({self.n}/{c})={w:.2f}"
