import pandas as pd
from pathlib import Path
from shared.contracts import EvidenceCandidate

def cluster_wallets(transactions: list[dict]) -> dict:
    # Union complete components, including when a transaction joins existing
    # clusters through non-root members. Stable representatives aid replay.
    parent = {}

    def find(addr):
        while parent[addr] != addr:
            parent[addr] = parent[parent[addr]]
            addr = parent[addr]
        return addr

    for tx in transactions:
        inputs = tx.get("inputs", [])
        if len(inputs) > 1:
            for addr in inputs:
                parent.setdefault(addr, addr)
            roots = sorted({find(addr) for addr in inputs})
            for root in roots:
                parent[root] = roots[0]
    return {addr: find(addr) for addr in sorted(parent)}


def lookup_risk(address: str, *, csv_path=None) -> str:
    csv_path = Path(csv_path) if csv_path is not None else Path(__file__).parent.parent / "data" / "bitcoinheist_sample.csv"
    if not csv_path.exists():
        return "unknown"
    df = pd.read_csv(csv_path)
    match = df[df['address'] == address]
    return match.iloc[0]['label'] if not match.empty else "unknown"
