import pandas as pd
from pathlib import Path
from shared.contracts import EvidenceCandidate

def cluster_wallets(transactions: list[dict]) -> dict:
    clusters = {}
    for tx in transactions:
        inputs = tx.get("inputs", [])
        if len(inputs) > 1:
            existing = next((clusters[a] for a in inputs if a in clusters), inputs[0])
            for addr in inputs:
                clusters[addr] = existing
                
    for k, v in clusters.items():
        while v in clusters and clusters[v] != v:
            v = clusters[v]
        clusters[k] = v
    return clusters

def lookup_risk(address: str) -> str:
    csv_path = Path(__file__).parent.parent / "data" / "bitcoinheist_sample.csv"
    if not csv_path.exists():
        return "unknown"
    df = pd.read_csv(csv_path)
    match = df[df['address'] == address]
    return match.iloc[0]['label'] if not match.empty else "unknown"
